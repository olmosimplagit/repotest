import argparse
import random
import time
import smtplib
import dkim
from concurrent.futures import ThreadPoolExecutor
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid, formatdate
import os
import sys

YOUR_DOMAIN = "alphacrew.team"
DKIM_SELECTOR = "mail"

def load_lines(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_private_key(key_path):
    with open(key_path, 'rb') as f:
        return f.read()

def dkim_sign_message(msg_bytes, privkey_bytes):
    """Sign the message with DKIM using relaxed/relaxed canonicalization."""
    if not privkey_bytes:
        return msg_bytes

    # Headers to include in the signature (add more as needed)
    headers_to_sign = [
        b'from', b'to', b'subject', b'date',
        b'message-id', b'mime-version', b'content-type'
    ]

    signature = dkim.sign(
        message=msg_bytes,
        selector=DKIM_SELECTOR.encode(),
        domain=YOUR_DOMAIN.encode(),
        privkey=privkey_bytes,
        include_headers=headers_to_sign,
        canonicalize=(b'relaxed', b'relaxed')   # relaxed for both header and body
    )
    # Insert the DKIM header into the raw message
    lines = msg_bytes.split(b'\r\n')
    for i, line in enumerate(lines):
        if line == b'':
            break
    lines.insert(i, signature)
    signed_msg = b'\r\n'.join(lines)
    
    # Debug: print the DKIM signature (first 200 chars)
    print(f"🔏 DKIM Signature: {signature[:200]}...", flush=True)
    return signed_msg

def send_email_smtp(recipient, from_email, from_name, subject, html_body, privkey_bytes, smtp_server):
    sys.stdout.flush()
    print(f"🔹 Connecting to {recipient}...", flush=True)
    try:
        # Build message
        msg = MIMEMultipart()
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = recipient
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        msg['Message-ID'] = make_msgid(domain=YOUR_DOMAIN)
        msg.attach(MIMEText(html_body, 'html'))

        # Convert to bytes and sign
        raw_msg = msg.as_string().encode('utf-8')
        if privkey_bytes:
            raw_msg = dkim_sign_message(raw_msg, privkey_bytes)

        # Send via port 25 (no TLS)
        with smtplib.SMTP(smtp_server, 25, timeout=15) as server:
            server.sendmail(from_email, recipient, raw_msg)
        print(f"✅ Sent to {recipient} via {smtp_server}:25", flush=True)
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

def send_emails_in_parallel(args, email_list, privkey_bytes, smtp_server):
    failed = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(
                send_email_smtp,
                r, args.from_email, n, s, args.html_body, privkey_bytes, smtp_server
            )
            for (r, n, s) in email_list
        ]
        time.sleep(0.1)
        for i, future in enumerate(futures):
            if not future.result():
                failed.append(email_list[i])
    return failed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--recipients', required=True)
    parser.add_argument('--html', required=True)
    parser.add_argument('--froms', required=True)
    parser.add_argument('--subjects', required=True)
    parser.add_argument('--smtp-server', required=True)
    parser.add_argument('--dkim-key', required=True)
    parser.add_argument('--threads', type=int, default=100)
    parser.add_argument('--max-retries', type=int, default=3)
    args = parser.parse_args()

    # Verify all input files exist
    for f in [args.recipients, args.html, args.froms, args.subjects, args.dkim_key]:
        if not os.path.exists(f):
            print(f"❌ File not found: {f}")
            sys.exit(1)

    recipients = load_lines(args.recipients)
    from_names = load_lines(args.froms)
    subjects = load_lines(args.subjects)
    with open(args.html, 'r') as f:
        args.html_body = f.read()
    privkey_bytes = load_private_key(args.dkim_key)

    if not recipients or not from_names or not subjects:
        print("❌ Input files empty")
        sys.exit(1)

    random_id = random.randint(100, 9999)
    args.from_email = f"rewards-{random_id}@{YOUR_DOMAIN}"

    print(f"📧 From: {random.choice(from_names)} <{args.from_email}>", flush=True)
    print(f"📝 Subject: {random.choice(subjects)}", flush=True)
    print(f"📨 Recipients: {len(recipients)}", flush=True)
    print(f"🔏 DKIM signing ON (selector={DKIM_SELECTOR}, domain={YOUR_DOMAIN})", flush=True)
    print(f"📡 Using SMTP server: {args.smtp_server}:25 (no STARTTLS)", flush=True)

    email_list = [(r, random.choice(from_names), random.choice(subjects)) for r in recipients]

    print("\n📤 Starting send...", flush=True)
    failed = send_emails_in_parallel(args, email_list, privkey_bytes, args.smtp_server)

    for attempt in range(args.max_retries):
        if not failed:
            break
        print(f"\n🔄 Retry {attempt+1}/{args.max_retries}, {len(failed)} left", flush=True)
        failed = send_emails_in_parallel(args, failed, privkey_bytes, args.smtp_server)

    if failed:
        print(f"\n❌ {len(failed)} emails permanently failed", flush=True)
    else:
        print("\n🎉 All emails sent successfully!", flush=True)

if __name__ == "__main__":
    main()