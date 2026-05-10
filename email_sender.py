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
DKIM_SELECTOR = "mail"                # <-- CHANGE to your selector, e.g. "mail"
DKIM_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQDKUD0EY6xh22cE5p4BmS0d5BNbdyuO3HhleCAa6xl9qHWhcN0P
GulAFRuehQRDr4gS1wY8dRYn630PjLOH+Hu0tl5d4C8OjTaho5dQ46Kejp2E13zo
I0b/iaEF4uCeHV5/X6JCOCXWftsER2B5WJbhVUXCmYLL1KWhTlj/e9h+tQIDAQAB
AoGAfYVc5h1FNY2flB3VSJ6VrGb2T5hXcRJ+rE3kdW8J6LmdCeXxcU68CuNNuINE
yw3b+fxoxRfMAEaN2Bjuxly3uqMb+RLp4khVKIgOUJ1ONnmihVecr3ohbBHPSDnB
z/y4i90cv7mpLmObxWCLGPoGVWq1xc27qNWu8VzW8Lak3F0CQQDz6PgHf4vddhJw
Wua6KVdIL99dwo0X08H8APX5EtxgTH5qajCB59mQXvjSbhwH2qa32HFXunCPEo+U
pzjiPFtfAkEA1FdwxUgd9MQF4+UxSwHR/RfOs1rNIoz4hD32793TYGC7JOaYHY2Z
oHHz0d9CYWevHXd9CswPr8awhGJ36NJyawJBAKdkPjxfI2z0aEkliW0/jAAloqTl
LRGqKVo6ipTKheWs+aEsiWfN5zk2hIteN+yH+Zz4dSjg8fiuo01AykAxbf8CQGXp
aahlymrVQfZ048maIAyWxo/yPo4clpHxo3jQQEj7ZBZ7zfoxIdCNoHXT72oMd1Fv
LcZm1giJFeMT13UYu+0CQBMW/P+/n7Cnr2McO0GTJoMUDmvV8hZeuLDLQtKAfmrC
5q907Wxp+Ba/KqYnrWBCeaDckXqPeN2ZvJd2o687gBI=
-----END RSA PRIVATE KEY-----
"""
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