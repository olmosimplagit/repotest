import argparse
import random
import time
import smtplib
import dns.resolver      # pip install dnspython
import dkim              # pip install dkimpy
from concurrent.futures import ThreadPoolExecutor
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# ========== YOUR DKIM CONFIGURATION (no longer hardcoded) ==========
# Domain and selector are still required for DKIM signing.
YOUR_DOMAIN = "alphacrew.team"           # <-- CHANGE to your domain
DKIM_SELECTOR = "mail"                   # <-- your DKIM selector
# ====================================================================

def load_lines(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_private_key(key_path):
    """Load DKIM private key from file, return as bytes."""
    with open(key_path, 'rb') as f:
        return f.read()

def dkim_sign_message(msg_bytes, privkey_bytes):
    """Apply DKIM signature using the provided private key."""
    if not privkey_bytes:
        return msg_bytes
    signature = dkim.sign(
        message=msg_bytes,
        selector=DKIM_SELECTOR.encode(),
        domain=YOUR_DOMAIN.encode(),
        privkey=privkey_bytes,
        include_headers=[b'from', b'to', b'subject', b'date']
    )
    # Insert the DKIM signature header into the raw message
    lines = msg_bytes.split(b'\r\n')
    for i, line in enumerate(lines):
        if line == b'':
            break
    lines.insert(i, signature)
    return b'\r\n'.join(lines)

def lookup_mx(domain):
    """Return the MX hostname with lowest preference for a domain."""
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        mx = sorted(answers, key=lambda r: r.preference)[0]
        return str(mx.exchange).rstrip('.')
    except Exception as e:
        print(f"⚠️ MX lookup failed for {domain}: {e}")
        return None

def send_email_direct(recipient, from_email, from_name, subject, html_body, privkey_bytes):
    """Deliver email directly to recipient's MX server (port 25)."""
    recipient_domain = recipient.split('@')[-1]
    mx_host = lookup_mx(recipient_domain)
    if not mx_host:
        return True   # treat as permanent failure

    try:
        # Build message
        msg = MIMEMultipart()
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        raw_msg = msg.as_string().encode('utf-8')
        if privkey_bytes:
            raw_msg = dkim_sign_message(raw_msg, privkey_bytes)

        with smtplib.SMTP(mx_host, 25, timeout=30) as server:
            server.ehlo()
            if server.has_extn("starttls"):
                server.starttls()
                server.ehlo()
            server.sendmail(from_email, recipient, raw_msg)
        print(f"✅ Sent to {recipient} via MX {mx_host}")
        return True
    except smtplib.SMTPResponseException as e:
        if 450 <= e.smtp_code <= 499:   # temporary failure
            print(f"🔄 Temp error for {recipient}: {e.smtp_code}")
            return False
        else:
            print(f"✉️ Bounced from {recipient}: {e.smtp_code} {str(e)}")
            return True
    except Exception as e:
        print(f"⚠️ Failed to send to {recipient}: {str(e)}")
        return True

def send_email_smtp(recipient, from_email, from_name, subject, html_body, privkey_bytes, smtp_server):
    """Send email via a central SMTP server (with STARTTLS on port 587)."""
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        raw_msg = msg.as_string().encode('utf-8')
        if privkey_bytes:
            raw_msg = dkim_sign_message(raw_msg, privkey_bytes)

        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.sendmail(from_email, recipient, raw_msg)
        print(f"✅ Sent to {recipient} via {smtp_server}")
        return True
    except smtplib.SMTPResponseException as e:
        if 450 <= e.smtp_code <= 499:
            return False
        else:
            print(f"✉️ Bounced from {recipient}: {e.smtp_code} {str(e)}")
            return True
    except Exception as e:
        print(f"⚠️ Failed to send to {recipient}: {str(e)}")
        return True

def send_emails_in_parallel(args, email_list, privkey_bytes, smtp_server, use_mx):
    failed = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for recipient, from_name, subject in email_list:
            if use_mx:
                futures.append(executor.submit(
                    send_email_direct,
                    recipient, args.from_email, from_name, subject,
                    args.html_body, privkey_bytes
                ))
            else:
                futures.append(executor.submit(
                    send_email_smtp,
                    recipient, args.from_email, from_name, subject,
                    args.html_body, privkey_bytes, smtp_server
                ))
            time.sleep(0.1)   # slight delay to avoid overwhelming

        for i, future in enumerate(futures):
            if not future.result():
                failed.append(email_list[i])
    return failed

def main():
    parser = argparse.ArgumentParser(description='Bulk email with DKIM and optional MX delivery')
    parser.add_argument('--recipients', required=True, help='File with recipient email addresses')
    parser.add_argument('--html', required=True, help='HTML email template file')
    parser.add_argument('--froms', required=True, help='File with display names')
    parser.add_argument('--subjects', required=True, help='File with subject lines')
    parser.add_argument('--smtp-server', help='SMTP server (required if --use-mx not given)')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads')
    parser.add_argument('--max-retries', type=int, default=3, help='Max retries per email')
    parser.add_argument('--dkim-key', required=True, help='Path to DKIM private key file (PEM)')
    parser.add_argument('--use-mx', action='store_true', help='Deliver directly via MX instead of SMTP server')
    args = parser.parse_args()

    # Validation
    if not args.use_mx and not args.smtp_server:
        print("❌ Either provide --smtp-server or use --use-mx flag")
        exit(1)
    for f in [args.recipients, args.html, args.froms, args.subjects, args.dkim_key]:
        if not os.path.exists(f):
            print(f"❌ File not found: {f}")
            exit(1)

    # Load data
    recipients = load_lines(args.recipients)
    from_names = load_lines(args.froms)
    subjects = load_lines(args.subjects)
    with open(args.html, 'r') as f:
        args.html_body = f.read()
    privkey_bytes = load_private_key(args.dkim_key)

    if not recipients or not from_names or not subjects:
        print("❌ One or more input files empty")
        exit(1)

    # Generate sender email
    random_id = random.randint(100, 9999)
    args.from_email = f"rewards-{random_id}@{YOUR_DOMAIN}"

    print(f"📧 From: {random.choice(from_names)} <{args.from_email}>")
    print(f"📝 Subject: {random.choice(subjects)}")
    print(f"📨 Recipients: {len(recipients)}")
    print(f"🔏 DKIM signing ON (selector={DKIM_SELECTOR}, domain={YOUR_DOMAIN})")
    if args.use_mx:
        print("🚀 Using direct MX delivery")
    else:
        print(f"📡 Using SMTP server: {args.smtp_server}")

    email_list = [(r, random.choice(from_names), random.choice(subjects)) for r in recipients]

    print("\n📤 Starting send...")
    failed = send_emails_in_parallel(args, email_list, privkey_bytes, args.smtp_server, args.use_mx)

    # Retry loop (only temporary failures are retried)
    for attempt in range(args.max_retries):
        if not failed:
            break
        print(f"\n🔄 Retry {attempt+1}/{args.max_retries}, {len(failed)} left")
        failed = send_emails_in_parallel(args, failed, privkey_bytes, args.smtp_server, args.use_mx)

    if failed:
        print(f"\n❌ {len(failed)} emails permanently failed")
    print("\n🎉 Done")

if __name__ == "__main__":
    main()