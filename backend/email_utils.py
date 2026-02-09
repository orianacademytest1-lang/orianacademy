import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database import get_smtp_settings

def send_notification_email(subject, data, type='contact'):
    """Send a notification email using SMTP settings from DB"""
    settings = get_smtp_settings()
    
    sender_email = settings.get('smtp_email')
    password = settings.get('smtp_password')
    receiver_email = settings.get('receiver_email')

    if not all([sender_email, password, receiver_email]):
        print("⚠️ SMTP settings not configured. Skipping email notification.")
        return False

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Oriana Academy: {subject}"

    # Format body
    if type == 'contact':
        body = f"""
New Contact Submission:
-----------------------
Name: {data.get('name')}
Email: {data.get('email')}
Phone: {data.get('phone')}
Subject: {data.get('subject')}

Message:
{data.get('message')}
"""
    else:  # enrollment
        body = f"""
New Enrollment Submission:
--------------------------
Name: {data.get('name')}
Email: {data.get('email')}
Phone: {data.get('phone')}
Interested Course: {data.get('course')}

Message:
{data.get('message', 'N/A')}
"""

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail SMTP (default)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email notification sent to {receiver_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
