import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database import get_smtp_settings

def send_notification_email(subject, data, type='contact'):
    """Send a notification email using SMTP settings from DB"""
    try:
        settings = get_smtp_settings()
        
        sender_email = settings.get('smtp_email')
        password = settings.get('smtp_password')
        receiver_email = settings.get('receiver_email')

        if not all([sender_email, password, receiver_email]):
            print("⚠️ SMTP settings not configured. Skipping email notification.")
            return False, "SMTP settings not configured."

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

        # Try Port 587 (TLS) first
        try:
            print(f"📧 Attempting to send email via port 587 (TLS)...")
            server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()
        except Exception as e587:
            print(f"⚠️ Port 587 failed: {e587}. Trying Port 465 (SSL)...")
            # Fallback to Port 465 (SSL)
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15)
            server.login(sender_email, password)
            server.send_message(msg)
            server.quit()

        print(f"✅ Email notification sent to {receiver_email}")
        return True, "Email sent successfully"
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Failed to send email: {error_msg}")
        return False, error_msg
