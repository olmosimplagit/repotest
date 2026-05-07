import argparse
import random
import time
from concurrent.futures import ThreadPoolExecutor
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random

list_of_domains = [

'aginghealthytoday.com',
'call-centre-software.com',
'homeguideguru.com',
'houselifetoday.com',
'justvegantoday.com',
'marcapelli.com',
'odetiah.com',
'pengenbeli.com',
'puppiesandpooches.com',
'relationshipsmag.com',
'sciencerecent.com',
'soundtrackworld.com',
'ssyyi.com',
'topshapenow.com',
'trading-systems-indicators.com',
'trailsjourney.com',
'travelingtodaymag.com',
'wallpapersfreak.com',
'ziggiesocial.com',
'123-stargate.net',
'boldwear.cz',
'clocktravel.rs',
'dipit.fi',
'euroinvent.org',
'healthyfoodsmag.net',
'homeguidetoday.net',
'klickfliessband.de',
'mac-lose.net',
'recreationtime.net',
'shimlys-drachenhort.de',
'simplygeeky.net',
'yoga.nl',
'yourmoneytoday.net',

]

def load_lines(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def send_email(args, recipient, from_name, from_email, subject):
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Read HTML body
        with open(args.html, 'r') as f:
            html_body = f.read()
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        with smtplib.SMTP(args.smtp_server, 25) as server:
            server.starttls()
            server.send_message(msg)
        
        print(f"✅ Sent to {recipient}")
        return True
    except smtplib.SMTPResponseException as e:
        # Check if it's a temporary error (4xx code)
        if e.smtp_code >= 450 and e.smtp_code <= 499:
            print(f"🔄 Temporary error for {recipient}: {e.smtp_code}")
            return False  # Return False to indicate it should be retried
        else:
            print(f"✉️ Bounced from {recipient}: {e.smtp_code} {str(e)}")
            return True
    except Exception as e:
        print(f"⚠️ Failed to send to {recipient}: {str(e)}")
        return True

def send_emails_in_parallel(args, email_list):
    """Send emails using thread pool with the given list of (recipient, from_name, subject) tuples"""
    failed_emails = []
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for recipient, from_name, subject in email_list:
            futures.append(executor.submit(
                send_email, 
                args, 
                recipient, 
                from_name, 
                args.from_email, 
                subject
            ))
            time.sleep(0.1)  # Small delay to avoid overwhelming the server

        # Collect results and track temporary failures
        for i, future in enumerate(futures):
            success = future.result()
            if not success:
                # Add the failed email to retry list
                failed_emails.append(email_list[i])
    
    return failed_emails

def main():
    parser = argparse.ArgumentParser(description='Send bulk emails with threading')
    parser.add_argument('--recipients', required=True, help='Path to recipients file')
    parser.add_argument('--html', required=True, help='Path to HTML email template')
    parser.add_argument('--froms', required=True, help='Path to from names file')
    parser.add_argument('--subjects', required=True, help='Path to subject lines file')
    parser.add_argument('--smtp-server', required=True, help='SMTP server address')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads to use')
    parser.add_argument('--max-retries', type=int, default=3, help='Maximum number of retry attempts')
    args = parser.parse_args()

    # Verify files exist
    for f in [args.recipients, args.html, args.froms, args.subjects]:
        if not os.path.exists(f):
            print(f"❌ File not found: {f}")
            exit(1)

    # Load data
    recipients = load_lines(args.recipients)
    from_names = load_lines(args.froms)
    subjects = load_lines(args.subjects)
    
    if not recipients or not from_names or not subjects:
        print("❌ One or more input files are empty")
        exit(1)

    # Generate random from email
    random_id = random.randint(100, 999)
    random_id_dm = random.randint(0, 35)
    dm = list_of_domains[random_id_dm]
    args.from_email = f"rewards-{random_id}@{dm}"

    print(f"📧 From: {random.choice(from_names)} <{args.from_email}>")
    print(f"📝 Subject: {random.choice(subjects)}")
    print(f"📨 Total recipients: {len(recipients)}")
    print(f"🧵 Using {args.threads} threads")
    print(f"🔄 Max retries: {args.max_retries}")

    # Prepare initial email list
    email_list = []
    for recipient in recipients:
        from_name = random.choice(from_names)
        subject = random.choice(subjects)
        email_list.append((recipient, from_name, subject))

    # Initial send
    print("\n📤 Starting initial send...")
    failed_emails = send_emails_in_parallel(args, email_list)
    print(f"Initial send completed. {len(failed_emails)} emails need retry.")

    # Retry loop
    for retry_attempt in range(args.max_retries):
        if not failed_emails:
            break
            
        print(f"\n🔄 Retry attempt {retry_attempt + 1}/{args.max_retries} with {len(failed_emails)} emails")
        failed_emails = send_emails_in_parallel(args, failed_emails)

    if failed_emails:
        print(f"\n❌ {len(failed_emails)} emails failed after all retry attempts")

    print("\n🎉 Email sending completed!")

if __name__ == "__main__":
    main()