def generate_payment_confirmation_email(fullname, price, reference, plan):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Recipes</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            background-color: #FFFFFF;
            color: #000000;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #FFFFFF;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #FF6347;
        }}
        .hero-image {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .feature-list {{
            background-color: #F8F8F8;
            padding: 20px;
            border-radius: 8px;
        }}
        .footer {{
            text-align: center;
            font-size: 14px;
            color: #333333;
            margin-top: 30px;
        }}
    </style>
    </head>
    <body>
    <div class="container">
        <h1>{reference} Confirmed!</h1>
        <img src="https://opendoodles.s3-us-west-1.amazonaws.com/loving.png" alt="Welcome to Recipes!" class="hero-image">
        <p>Hello, {fullname}!</p>
        <p>A payment for our {plan} was received successfully! We received {price}</p>
        
        <h2>🍽️ What You Can Do:</h2>
        <div class="feature-list">
            <ul>
                <li>📝 Create and edit mouth-watering recipes</li>
                <li>📸 Upload high-quality food images</li>
                <li>👤 Manage user accounts and reviews</li>
                <li>📊 Access analytics on your recipes</li>
                <li>🏷️ Organize recipes with tags and categories</li>
                <li>📢 Publish special announcements and featured recipes</li>
                <li>📢 Enjoy Ad-Free moments.</li>
            </ul>
        </div>

        <p>To help you get started, we've prepared a special treat just for you:</p>
        <img src="https://opendoodles.s3-us-west-1.amazonaws.com/clumsy.png" alt="Your user Toolkit" style="width: 100%; height: auto; border-radius: 8px; margin: 20px 0;">

        <p>This is your user toolkit, packed with all the resources you need to start cooking up a storm in our digital kitchen!</p>

        <p>If you have any questions or need assistance, our support team is always ready to help. Just drop us a line at <strong>support@recipes.com</strong>.</p>

        <div class="footer">
            <p>Happy cooking and welcome aboard!</p>
            <p>The Recipes Team</p>
        </div>
    </div>
    </body>
    </html>
    """
    return html_content