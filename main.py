import requests
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")
GMAIL_KEY = os.getenv("GMAIL_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def gold_course(currency, unit):
    url = "https://api.metals.dev/v1/latest"
    params = {
        "api_key": API_KEY,
        "currency": currency,
        "unit": unit
        }
    response = requests.get(url, params=params)
    data = (response.json())
    pln_xau_rate = round(data["metals"].get("gold"), 2)
    return pln_xau_rate


def send_email():
    gold_rate = gold_course(currency="PLN", unit="toz")
    subject = "Gold Rate Update for Today"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>📈 Today's Gold Rate</h2>
        <p>Hello,</p>
        <p>Here is the latest update on the gold rate:</p>
        <table style="border: 1px solid #ccc; padding: 10px; margin-top: 10px;">
            <tr>
                <td style="padding: 8px;"><strong>Gold Rate (1 oz):</strong></td>
                <td style="padding: 8px;">{gold_rate} PLN</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>Date:</strong></td>
                <td style="padding: 8px;">{datetime.now().strftime('%d-%m-%Y')}</td>
            </tr>
        </table>
    </body>
    </html>
    """

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    #msg.set_content(body)
    msg.add_alternative(body, subtype='html')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, GMAIL_KEY)
        smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    
    print("Email was correctly sent.")

send_email()