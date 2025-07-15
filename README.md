
# Naukri Profile Auto-Updater

This project automates the process of refreshing your Naukri profile every X minutes using GitHub Actions and Selenium.

## Features

- Headless browser automation with Selenium
- Retry mechanism on failure
- Email notifications on failure (via Gmail)
- Scheduled GitHub Actions (CRON)

## Setup

### 1. GitHub Secrets

Go to `Settings > Secrets > Actions` in your GitHub repository and add the following secrets:

- `NAUKRI_USERNAME`: Your Naukri email/username
- `NAUKRI_PASSWORD`: Your Naukri password
- `ALERT_EMAIL_FROM`: Sender email address (Gmail recommended)
- `ALERT_EMAIL_TO`: Receiver email address
- `EMAIL_APP_PASSWORD`: App password for sender email

### 2. Modify CRON Schedule

In `.github/workflows/update-profile.yml`, change the CRON syntax to control frequency.

### 3. Dependencies

- Python 3.x
- Selenium

Install via:
```
pip install -r requirements.txt
```

## How it Works

1. Logs in to your Naukri account
2. Navigates to the profile page
3. Clicks "Save" to refresh profile
4. Retries on failure (up to 3 times)
5. Sends email if all retries fail

---

**Note:** Use responsibly to avoid being flagged by Naukri.com for automated actions.
