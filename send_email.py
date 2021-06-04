import smtplib
from datetime import datetime
import logging
from systemd.journal import JournalHandler

class Emailer:
    def __init__(self):
        self.SMTP_SERVER = 'smtp.gmail.com'
        self.SMTP_PORT = 587
        self.GMAIL_USERNAME = ''
        self.GMAIL_PASSWORD = ''

        with open(".email_cred", "r") as f:
            self.GMAIL_USERNAME = f.readline().strip("\r\n")
            self.GMAIL_PASSWORD = f.readline().strip("\r\n")

    def sendmail(self, recipient, subject, content):
        # create headers
        headers = "\r\n".join([
                    "From: " + self.GMAIL_USERNAME,
                    "Subject: " + subject,
                    "To: " + recipient,
                    "MIME-Version: 1.0",
                    "Content-Type: text/html"])

        # connect to Gmail server
        session = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        # login to Gmail
        session.login(self.GMAIL_USERNAME, self.GMAIL_PASSWORD)

        # send email and exit
        session.sendmail(self.GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit()

def main():
    sender = Emailer()

    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S")

    log = logging.getLogger("send_email.py")
    log.addHandler(JournalHandler())
    log.setLevel(logging.INFO)

    sendTo = "dummy-email@gmail.com"
    emailSubject = "[Raspberry Pi | SSH Logger] SSH login"
    emailContent = "I got logged in via SSH at " + now

    sender.sendmail(sendTo, emailSubject, emailContent)
    log.info("SSH login - sent email at " + now)

if __name__ == "__main__":
    main()