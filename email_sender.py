import argparse
import random
import time
from concurrent.futures import ThreadPoolExecutor
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import dkim  # pip install dkimpy

# ========== YOUR DKIM CONFIGURATION ==========
YOUR_DOMAIN = "alphacrew.team"           # <-- CHANGE to your real domain
DKIM_SELECTOR = "s1"                # <-- CHANGE to your selector, e.g. "mail"
DKIM_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""
# ============================================

def load_lines(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def dkim_sign_message(msg_bytes, from_email):
    """Apply DKIM signature using the hardcoded private key."""
    if not DKIM_PRIVATE_KEY:
        return msg_bytes
    # Use your fixed domain (not the one from from_email)
    signing_domain = YOUR_DOMAIN
    signature = dkim.sign(
        message=msg_bytes,
        selector=DKIM_SELECTOR.encode(),
        domain=signing_domain.encode(),
        privkey=DKIM_PRIVATE_KEY.encode(),
        include_headers=[b'from', b'to', b'subject', b'date']
    )
    lines = msg_bytes.split(b'\r\n')
    for i, line in enumerate(lines):
        if line == b'':
            break
    lines.insert(i, signature)
    return b'\r\n'.join(lines)

def send_email(args, recipient, from_name, from_email, subject):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = recipient
        msg['Subject'] = subject
        with open(args.html, 'r') as f:
            html_body = f.read()
        msg.attach(MIMEText(html_body, 'html'))

        raw_msg = msg.as_string().encode('utf-8')
        if DKIM_PRIVATE_KEY:
            raw_msg = dkim_sign_message(raw_msg, from_email)

        with smtplib.SMTP(args.smtp_server, 25) as server:
            server.starttls()
            server.sendmail(from_email, recipient, raw_msg)
        print(f"✅ Sent to {recipient}")
        return True
    except smtplib.SMTPResponseException as e:
        if 450 <= e.smtp_code <= 499:
            print(f"🔄 Temporary error for {recipient}: {e.smtp_code}")
            return False
        else:
            print(f"✉️ Bounced from {recipient}: {e.smtp_code} {str(e)}")
            return True
    except Exception as e:
        print(f"⚠️ Failed to send to {recipient}: {str(e)}")
        return True

def send_emails_in_parallel(args, email_list):
    failed = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(send_email, args, r, n, args.from_email, s) for (r, n, s) in email_list]
        time.sleep(0.1)
        for i, f in enumerate(futures):
            if not f.result():
                failed.append(email_list[i])
    return failed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--recipients', required=True)
    parser.add_argument('--html', required=True)
    parser.add_argument('--froms', required=True)
    parser.add_argument('--subjects', required=True)
    parser.add_argument('--smtp-server', required=True)
    parser.add_argument('--threads', type=int, default=100)
    parser.add_argument('--max-retries', type=int, default=3)
    args = parser.parse_args()

    for f in [args.recipients, args.html, args.froms, args.subjects]:
        if not os.path.exists(f):
            print(f"❌ File not found: {f}")
            exit(1)

    recipients = load_lines(args.recipients)
    from_names = load_lines(args.froms)
    subjects = load_lines(args.subjects)

    if not recipients or not from_names or not subjects:
        print("❌ Input files empty")
        exit(1)

    # Use YOUR domain for the From address (mandatory for DKIM)
    random_id = random.randint(100, 9999)
    args.from_email = f"rewards-{random_id}@{YOUR_DOMAIN}"

    print(f"📧 From: {random.choice(from_names)} <{args.from_email}>")
    print(f"📝 Subject: {random.choice(subjects)}")
    print(f"📨 Recipients: {len(recipients)}")
    print(f"🔏 DKIM signing ON (selector={DKIM_SELECTOR}, domain={YOUR_DOMAIN})")

    email_list = [(r, random.choice(from_names), random.choice(subjects)) for r in recipients]

    print("\n📤 Sending...")
    failed = send_emails_in_parallel(args, email_list)

    for attempt in range(args.max_retries):
        if not failed:
            break
        print(f"\n🔄 Retry {attempt+1}/{args.max_retries}, {len(failed)} left")
        failed = send_emails_in_parallel(args, failed)

    if failed:
        print(f"\n❌ {len(failed)} emails permanently failed")
    print("\n🎉 Done")

if __name__ == "__main__":
    main()