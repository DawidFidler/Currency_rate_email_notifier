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


def get_metal_rate(currency, unit, metal):
    url = "https://api.metals.dev/v1/latest"
    params = {
        "api_key": API_KEY,
        "currency": currency,
        "unit": unit
        }
    response = requests.get(url, params=params)
    data = (response.json())
    return data["metals"].get(metal)


def get_currencies_rate(base, currency_symbol):
    url = "https://api.metals.dev/v1/currencies"
    params = {
        "api_key": API_KEY,
        "base": base
    }
    response = requests.get(url, params=params)
    data = (response.json())
    return data["currencies"].get(currency_symbol)


def send_email():
    gold_rate = round(get_metal_rate(currency="PLN", unit="toz", metal="gold"), 2)
    euro_rate = round(get_currencies_rate(base="PLN", currency_symbol="EUR"), 3)
    dollar_rate = round(get_currencies_rate(base="PLN", currency_symbol="USD"), 3)
    franc_rate = round(get_currencies_rate(base="PLN", currency_symbol="CHF"), 3)
    subject = "🪙💵Daily Gold&Currency rates📈📉"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2>Gold&Currency Rates</h2>
        <table style="border: 1px solid #ccc; padding: 10px; margin-top: 10px;">
            <tr>
                <td style="padding: 8px;"><strong>Date:</strong></td>
                <td style="padding: 8px;">{datetime.now().strftime('%d-%m-%Y')}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>Gold rate (1 oz):</strong></td>
                <td style="padding: 8px;">{gold_rate} PLN</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>Euro rate:</strong></td>
                <td style="padding: 8px;">{euro_rate} PLN</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>US Dollar rate:</strong></td>
                <td style="padding: 8px;">{dollar_rate} PLN</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>Switzerland Franc rate:</strong></td>
                <td style="padding: 8px;">{franc_rate} PLN</td>
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