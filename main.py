import requests
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl #doczytać -> standard technology for kipping internet connection secure and safeguarding any data that is being sent to systems
import smtplib


def gold_course(base, currency):
    url = "https://api.metalpriceapi.com/v1/latest"
    params = {
        "api_key": api_key,
        "base": base,
        "currencies": currency
        }
    response = requests.get(url, params=params)
    data = (response.json())
    pln_xau_rate = round(data["rates"].get("PLNXAU"), 2)
    return pln_xau_rate


load_dotenv()
api_key = os.getenv("API_KEY")
gmail_key = os.getenv("GMAIL_KEY")
email_sender = os.getenv("EMAIL_SENDER")
email_receiver = os.getenv("EMAIL_RECEIVER")


def send_email():
    gold_rate = gold_course(base="PLN", currency="XAU")
    subject = "Tygodniowy kurs złota"
    body = f"""
    Kurs uncji złota na dziś wynosi: {gold_rate}zł.
    """

    msg = EmailMessage()
    msg["From"] = email_sender
    msg["To"] = email_receiver
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_sender, gmail_key)
        smtp.sendmail(email_sender, email_receiver, msg.as_string())
    print("Email was correctly sent.")

send_email()