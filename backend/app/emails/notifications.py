# emails/notifications.py

from flask import jsonify
import resend
import os

resend.api_key = os.environ["RESEND_API_KEY"]

def send_email(to, subject, html_content):
    params = {
        "from": "Davies Evan <onboarding@resend.dev>",
        "to": to,
        "subject": subject,
        "html": html_content
    }
    
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return jsonify(message=f"Email sent to {to}"), 200
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify(message=f"Failed to send email to {to}"), 500



