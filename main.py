import requests
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib

load_dotenv()
API_KEY = os.getenv("API_KEY")
GMAIL_KEY = os.getenv("GMAIL_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def gold_course(base, currency):
    url = "https://api.metalpriceapi.com/v1/latest"
    params = {
        "api_key": API_KEY,
        "base": base,
        "currencies": currency
        }
    response = requests.get(url, params=params)
    data = (response.json())
    pln_xau_rate = round(data["rates"].get("PLNXAU"), 2)
    print("Response data", data)
    return pln_xau_rate


def send_email():
    gold_rate = gold_course(base="PLN", currency="XAU")
    subject = "Tygodniowy kurs złota"
    body = f"""
    Kurs uncji złota na dziś wynosi: {gold_rate}zł.
    """

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, GMAIL_KEY)
        smtp.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    
    print("Email was correctly sent.")

send_email()
