# Gold & Currency Rates Email Notifier

This project is a Python script that retrieves the current rates for gold and major currencies (EUR, USD, and CHF) in PLN using th [Metals API](https://metals.dev/). The script then sends these rates via email in a formatted HTML table. It is designed to run on a daily schedule using GitHub Actions, enabling fully automated, daily notifications.

## Features

- Fetches the current rates for:
    - Gold (per ounce)
    - Euro (EUR)
    - US Dollar (USD)
    - Swiss Franc (CHF)
- Sends an email notification with a formatted HTML table of the latest rates.
- Uses environment variables to securely access API keys and email credentials.
- Runs automatically at a specified time each day through GitHub Actions.

## Requirements

- Python 3.11
- [Metals API](https://metals.dev/) account (for the `API_KEY`).
- Gmail account for sending emails (for the `GMAIL_KEY`).
- GitHub account to set up GitHub Actions.
