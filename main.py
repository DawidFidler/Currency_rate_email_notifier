import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
import requests
from dotenv import load_dotenv

load_dotenv()

REQUEST_TIMEOUT = 5


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_metal_rate(api_key: str, metal: str, currency: str) -> float:
    url = "https://api.metals.dev/v1/metal/spot"
    params = {
        "api_key": api_key,
        "metal": metal,
        "currency": currency,
    }
    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    rate = data.get("rate") if isinstance(data, dict) else None
    if not isinstance(rate, dict) or "price" not in rate:
        raise ValueError("Unexpected metals API response: missing rate.price.")
    return rate["price"]


def get_currency_rate(api_key: str, base: str) -> dict[str, float]:
    url = "https://api.metals.dev/v1/currencies"
    params = {
        "api_key": api_key,
        "base": base,
    }
    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    currencies = data.get("currencies") if isinstance(data, dict) else None
    if not isinstance(currencies, dict):
        raise ValueError("Unexpected metals API response: missing currencies.")
    return currencies


def send_email() -> None:
    api_key = _required_env("API_KEY")
    gmail_key = _required_env("GMAIL_KEY")
    sender_email = _required_env("EMAIL_SENDER")
    receiver_email = _required_env("EMAIL_RECEIVER")

    gold_rate = round(get_metal_rate(api_key=api_key, metal="gold", currency="PLN"), 2)
    currencies = get_currency_rate(api_key=api_key, base="PLN")
    euro_rate = round(currencies["EUR"], 2)
    dollar_rate = round(currencies["USD"], 2)
    franc_rate = round(currencies["CHF"], 2)
    now = datetime.now()

    subject = "🪙💵Daily Gold&Currency rates📈📉"
    text_body = f"""Gold and currency rates
Date: {now.strftime('%d-%m-%Y')}
Time: {now.strftime('%H:%M')}
Gold (1 oz): {gold_rate} PLN
Euro: {euro_rate} PLN
US Dollar: {dollar_rate} PLN
Swiss Franc: {franc_rate} PLN
"""
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <table style="border: 1px solid #ccc; padding: 10px; margin-top: 10px;">
            <tr>
                <td style="padding: 8px;"><strong>Date:</strong></td>
                <td style="padding: 8px;">{now.strftime('%d-%m-%Y')}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>Time:</strong></td>
                <td style="padding: 8px;">{now.strftime('%H:%M')}</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>Gold (1 oz):</strong></td>
                <td style="padding: 8px;">{gold_rate} PLN</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>Euro:</strong></td>
                <td style="padding: 8px;">{euro_rate} PLN</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>US Dollar:</strong></td>
                <td style="padding: 8px;">{dollar_rate} PLN</td>
            </tr>
            <tr>
                <td style="padding: 8px;"><strong>Swiss Franc:</strong></td>
                <td style="padding: 8px;">{franc_rate} PLN</td>
            </tr>
        </table>
    </body>
    </html>
    """

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=REQUEST_TIMEOUT) as smtp:
        smtp.login(sender_email, gmail_key)
        smtp.send_message(msg)

    print("Email was correctly sent.")


if __name__ == "__main__":
    send_email()
