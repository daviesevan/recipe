def generate_password_reset_email(user, reset_code):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset Code</title>
    <style>
        body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        background-color: #1f2937; 
        color: #e5e7eb; 
        margin: 0;
        padding: 20px;
        }}
        .container {{
        max-width: 600px;
        margin: 0 auto;
        background-color: #111827; 
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .code {{
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        padding: 20px;
        background-color: #374151; 
        border-radius: 8px;
        }}
        .footer {{
        text-align: center;
        font-size: 14px;
        color: #6b7280; 
        }}
    </style>
    </head>
    <body>
    <div class="container">
        <h1>Password Reset Code</h1>
        <p>Hello, {user.fullname}</p>
        <p>You have requested to reset your password. Please use the following 6-digit code to proceed:</p>
        <div class="code">{ reset_code }</div>
        <p>This code will expire in 15 minutes.</p>
        <div class="footer">
        If you didn't request a password reset, please ignore this email.
        </div>
    </div>
    </body>
    </html>
    """
    return html_content
