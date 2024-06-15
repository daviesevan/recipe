def generate_welcome_email(user):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
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
        .footer {{
        text-align: center;
        font-size: 14px;
        color: #6b7280; 
        }}
    </style>
    </head>
    <body>
    <div class="container">
        <h1>Welcome to Our Company</h1>
        <p>Hello, {user.fullname}</p>
        <p>Welcome to the team! We are excited to have you on board. Feel free to reach out if you have any questions.</p>
        <div class="footer">
        If you have any questions, please don't hesitate to contact us.
        </div>
    </div>
    </body>
    </html>
    """
    return html_content
