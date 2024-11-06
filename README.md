# Gold Rate Email Notifier

This project is a Python script that retrieves the current gold rate (in PLN) using the [Metals API](https://metals.dev/) and sends the rate via email. The script is designed to run on a daily schedule using GitHub Actions, allowing it to automatically send the email without manual intervention.

## Features

- Fetches the current gold rate from the Metals API.
- Sends an email notification with the latest gold rate.
- Uses environment variables for secure access to API keys and email credentials.
- Runs automatically at a specified time each day through GitHub Actions.

## Requirements

- Python 3.11
- [Metals API](https://metals.dev/) account (for the `API_KEY`).
- Gmail account for sending emails (for the `GMAIL_KEY`).
- GitHub account to set up GitHub Actions.
