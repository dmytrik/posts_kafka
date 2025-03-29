import logging
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

smtp_server = settings.email_host
smtp_port = settings.email_port
username = settings.email_user
password = settings.email_password
receiver = settings.email_receiver

async def send_email(body: str):

    try:
        logger.info(f"SMTP config: host={smtp_server}, port={smtp_port}, user={username}")
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = receiver
        msg["Subject"] = "Post Created"
        msg.attach(MIMEText(body, "plain"))

        loop = asyncio.get_event_loop()
        smtp = smtplib.SMTP(host=smtp_server, port=smtp_port, timeout=10)

        await loop.run_in_executor(None, smtp.connect, smtp_server, smtp_port)
        logger.info("Connected to SMTP server")

        await loop.run_in_executor(None, smtp.starttls)
        logger.info("STARTTLS activated")

        await loop.run_in_executor(None, smtp.login, username, password)
        logger.info("SMTP login successful")

        await loop.run_in_executor(None, smtp.sendmail, username, receiver, msg.as_string())
        logger.info(f"Email sent to {receiver}")

        await loop.run_in_executor(None, smtp.quit)
        logger.info("SMTP connection closed")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise