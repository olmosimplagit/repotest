import argparse
import random
import time
import smtplib
import dns.resolver
import dkim
from email.message import EmailMessage
from email.utils import make_msgid, formatdate
from concurrent.futures import ThreadPoolExecutor
import os
import sys

# ========== YOUR DKIM CONFIGURATION ==========
YOUR_DOMAIN = "alphacrew.team"
DKIM_SELECTOR = "mail"
# ============================================

def load_lines(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_private_key(key_path):
    with open(key_path, 'rb') as f:
        return f.read()

def build_message(from_addr, to_addr, subject, html_body, from_name):
    """Construct an EmailMessage with HTML content."""
    msg = EmailMessage()
    msg['From'] = f"{from_name} <{from_addr}>"
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid(domain=YOUR_DOMAIN)
    msg.set_content(html_body, subtype='html')   # HTML body
    return msg.as_bytes()

def dkim_sign(raw_message, privkey_bytes):
    """Sign the raw message with DKIM using relaxed/relaxed canonicalization."""
    headers = [b'from', b'to', b'subject', b'date', b'message-id', b'content-type']
    sig = dkim.sign(
        message=raw_message,
        selector=DKIM_SELECTOR.encode(),
        domain=YOUR_DOMAIN.encode(),
        privkey=privkey_bytes,
        include_headers=headers,
        canonicalize=(b'relaxed', b'relaxed')
    )
    # sig already contains the full DKIM-Signature header line (with CRLF)
    return sig + raw_message

def lookup_mx(domain):
    """Return the MX host with lowest preference."""
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        mx = sorted(answers, key=lambda r: r.preference)[0]
        return str(mx.exchange).rstrip('.')
    except Exception as e:
        print(f"⚠️ MX lookup failed for {domain}: {e}", flush=True)
        return None

def send_email_direct(recipient, from_email, from_name, subject, html_body, privkey_bytes):
    """Deliver directly to recipient's MX (port 25, opportunistic STARTTLS)."""
    sys.stdout.flush()
    recipient_domain = recipient.split('@')[-1]
    mx_host = lookup_mx(recipient_domain)
    if not mx_host:
        return True   # permanent failure

    print(f"🔹 Sending to {recipient} via MX {mx_host}...", flush=True)
    try:
        raw = build_message(from_email, recipient, subject, html_body, from_name)
        signed = dkim_sign(raw, privkey_bytes)

        with smtplib.SMTP(mx_host, 25, timeout=30) as server:
            server.ehlo()
            if server.has_extn("starttls"):
                server.starttls()
                server.ehlo()
            server.sendmail(from_email, recipient, signed)
        print(f"✅ Sent to {recipient} via MX", flush=True)
        return True
    except smtplib.SMTPResponseException as e:
        if 450 <= e.smtp_code <= 499:
            print(f"🔄 Temp error for {recipient}: {e.smtp_code}", flush=True)
            return False
        else:
            print(f"✉️ Bounced from {recipient}: {e.smtp_code} {str(e)}", flush=True)
            return True
    except Exception as e:
        print(f"⚠️ Failed to send to {recipient}: {str(e)}", flush=True)
        return True

def send_email_relay(recipient, from_email, from_name, subject, html_body, privkey_bytes, smtp_server):
    """Send via a relay SMTP server (port 25, no TLS, as requested)."""
    sys.stdout.flush()
    print(f"🔹 Sending to {recipient} via relay {smtp_server}:25...", flush=True)
    try:
        raw = build_message(from_email, recipient, subject, html_body, from_name)
        signed = dkim_sign(raw, privkey_bytes)

        with smtplib.SMTP(smtp_server, 25, timeout=15) as server:
            server.sendmail(from_email, recipient, signed)
        print(f"✅ Sent to {recipient}", flush=True)
        return True
    except smtplib.SMTPResponseException as e:
        if 450 <= e.smtp_code <= 499:
            print(f"🔄 Temp error for {recipient}: {e.smtp_code}", flush=True)
            return False
        else:
            print(f"✉️ Bounced from {recipient}: {e.smtp_code} {str(e)}", flush=True)
            return True
    except Exception as e:
        print(f"⚠️ Failed to send to {recipient}: {str(e)}", flush=True)
        return True

def send_emails_parallel(args, email_list, privkey_bytes, smtp_server=None, use_mx=False):
    failed = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for recipient, from_name, subject in email_list:
            if use_mx:
                fut = executor.submit(
                    send_email_direct,
                    recipient, args.from_email, from_name, subject,
                    args.html_body, privkey_bytes
                )
            else:
                fut = executor.submit(
                    send_email_relay,
                    recipient, args.from_email, from_name, subject,
                    args.html_body, privkey_bytes, smtp_server
                )
            futures.append(fut)
            time.sleep(0.05)   # slight delay

        for i, future in enumerate(futures):
            if not future.result():
                failed.append(email_list[i])
    return failed

def main():
    parser = argparse.ArgumentParser(description='Bulk email with DKIM (MX or relay)')
    parser.add_argument('--recipients', required=True)
    parser.add_argument('--html', required=True)
    parser.add_argument('--froms', required=True)
    parser.add_argument('--subjects', required=True)
    parser.add_argument('--smtp-server', help='SMTP relay server (required if not --use-mx)')
    parser.add_argument('--dkim-key', required=True)
    parser.add_argument('--threads', type=int, default=100)
    parser.add_argument('--max-retries', type=int, default=3)
    parser.add_argument('--use-mx', action='store_true', help='Deliver directly via MX instead of relay')
    args = parser.parse_args()

    # Validation
    if not args.use_mx and not args.smtp_server:
        print("❌ Either provide --smtp-server or use --use-mx", file=sys.stderr)
        sys.exit(1)
    for f in [args.recipients, args.html, args.froms, args.subjects, args.dkim_key]:
        if not os.path.exists(f):
            print(f"❌ File not found: {f}", file=sys.stderr)
            sys.exit(1)

    # Load data
    recipients = load_lines(args.recipients)
    from_names = load_lines(args.froms)
    subjects = load_lines(args.subjects)
    with open(args.html, 'r') as f:
        args.html_body = f.read()
    privkey_bytes = load_private_key(args.dkim_key)

    if not recipients or not from_names or not subjects:
        print("❌ One or more input files empty", file=sys.stderr)
        sys.exit(1)

    # Sender address
    random_id = random.randint(100, 9999)
    args.from_email = f"rewards-{random_id}@{YOUR_DOMAIN}"

    print(f"📧 From: {random.choice(from_names)} <{args.from_email}>", flush=True)
    print(f"📝 Subject: {random.choice(subjects)}", flush=True)
    print(f"📨 Recipients: {len(recipients)}", flush=True)
    print(f"🔏 DKIM: selector={DKIM_SELECTOR}, domain={YOUR_DOMAIN}", flush=True)
    if args.use_mx:
        print("🚀 Delivery: direct to MX (port 25, opportunistic STARTTLS)", flush=True)
    else:
        print(f"📡 Delivery: relay via {args.smtp_server}:25 (no TLS)", flush=True)

    # Prepare email list: (recipient, from_name, subject)
    email_list = [(r, random.choice(from_names), random.choice(subjects)) for r in recipients]

    print("\n📤 Starting send...", flush=True)
    failed = send_emails_parallel(args, email_list, privkey_bytes, args.smtp_server, args.use_mx)

    for attempt in range(args.max_retries):
        if not failed:
            break
        print(f"\n🔄 Retry {attempt+1}/{args.max_retries}, {len(failed)} remaining", flush=True)
        failed = send_emails_parallel(args, failed, privkey_bytes, args.smtp_server, args.use_mx)

    if failed:
        print(f"\n❌ {len(failed)} emails permanently failed", flush=True)
    else:
        print("\n🎉 All emails sent successfully!", flush=True)

if __name__ == "__main__":
    main()
