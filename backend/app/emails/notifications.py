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
    email = resend.Emails.send(params)
    print(email)
    
    return jsonify(message=f"Email sent to {to}"), 200


