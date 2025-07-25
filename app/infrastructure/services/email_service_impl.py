import aiosmtplib
from email.message import EmailMessage

from app.domain.services.email_service import EmailService


class EmailServiceImpl(EmailService):
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    async def send_email(self, to: str, subject: str, body: str):
        message = EmailMessage()
        message["From"] = self.username
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)

        await aiosmtplib.send(
            message,
            hostname=self.smtp_host,
            port=self.smtp_port,
            username=self.username,
            password=self.password,
            start_tls=True,
    )