
import os
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NaukriProfileUpdater:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self._init_driver()

    def _init_driver(self):
        chrome_options = Options()
        if os.getenv("HEADLESS", "false").lower() == "true":
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument(f"--user-data-dir=/tmp/chrome-user-data-{int(time.time())}")
        return webdriver.Chrome(options=chrome_options)


    def login(self):
        logging.info("Navigating to Naukri login page")
        self.driver.get("https://www.naukri.com/nlogin/login")
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "usernameField")))
            self.driver.find_element(By.ID, "usernameField").send_keys(self.username)
            self.driver.find_element(By.ID, "passwordField").send_keys(self.password)
            self.driver.find_element(By.XPATH, '//button[contains(text(),"Login")]').click()
        except Exception as e:
            logging.error(f"Login error: {e}")
            raise

    def update_profile(self):
        try:
            logging.info("Navigating to profile page")
            self.driver.get("https://www.naukri.com/mnjuser/profile")
            

            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@class='icon edit ']")))
            self.driver.find_element(By.XPATH, "//*[@class='icon edit ']").click()

            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, "root")))
            
            save_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'saveBasicDetailsBtn')))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
            time.sleep(1)  # slight delay to stabilize scroll
            self.driver.find_element(By.ID, 'saveBasicDetailsBtn').click()
            logging.info("Profile updated successfully.")
        except (TimeoutException, NoSuchElementException) as e:
            logging.error(f"Failed to update profile: {e}")
            raise

    def quit(self):
        self.driver.quit()

def send_email_alert(subject, body):
    from_email = os.getenv("ALERT_EMAIL_FROM")
    to_email = os.getenv("ALERT_EMAIL_TO")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(from_email, app_password)
        server.send_message(msg)
        server.quit()
        logging.info("Failure notification email sent.")
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

def main():
    username = os.getenv("NAUKRI_USERNAME")
    password = os.getenv("NAUKRI_PASSWORD")

    if not username or not password:
        logging.error("Username or password not found in environment variables")
        return

    max_retries = 3
    success = False

    for attempt in range(1, max_retries + 1):
        logging.info(f"Attempt {attempt} of {max_retries}")
        updater = NaukriProfileUpdater(username, password)
        try:
            updater.login()
            time.sleep(5)
            updater.update_profile()
            success = True
            break
        except Exception as e:
            logging.error(f"Attempt {attempt} failed: {e}")
        finally:
            updater.quit()
            time.sleep(10)

    if not success:
        subject = "❌ Naukri Profile Update Failed"
        body = "All attempts to update the Naukri profile have failed."
        send_email_alert(subject, body)

if __name__ == "__main__":
    main()
