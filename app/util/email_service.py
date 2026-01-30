import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import settings


BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, "email_templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"])
)


class EmailService:

    @staticmethod
    def _send(
        to_email: str,
        subject: str,
        html_body: str,
        attachment_bytes: bytes | None = None,
        attachment_name: str | None = None,
    ):
        # 🔹 Use mixed for attachments
        msg = MIMEMultipart("mixed")
        msg["From"] = f"{settings.EMAIL_USERNAME} <{settings.EMAIL_FROM}>"
        msg["To"] = to_email
        msg["Subject"] = subject

        # 🔹 HTML body
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        # 🔹 Attachment (optional)
        if attachment_bytes and attachment_name:
            part = MIMEApplication(attachment_bytes)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{attachment_name}"'
            )
            msg.attach(part)

        try:
            if settings.EMAIL_USE_SSL:
                server = smtplib.SMTP_SSL(
                    settings.EMAIL_HOST,
                    settings.EMAIL_PORT
                )
            else:
                server = smtplib.SMTP(
                    settings.EMAIL_HOST,
                    settings.EMAIL_PORT
                )
                server.starttls()

            with server:
                server.login(
                    settings.EMAIL_USERNAME,
                    settings.EMAIL_PASSWORD
                )
                server.send_message(msg)

        except Exception as e:
            raise RuntimeError(f"Email sending failed: {str(e)}")

    @classmethod
    def send_email(
        cls,
        to_email: str,
        subject: str,
        template_name: str,
        attachment_bytes: bytes | None = None,
        attachment_name: str | None = None,
        **template_vars,
    ):
        """
        template_name -> HTML file inside email_templates/
        template_vars -> injected into Jinja template
        """

        template = env.get_template(template_name)
        html_body = template.render(**template_vars)

        cls._send(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
            attachment_bytes=attachment_bytes,
            attachment_name=attachment_name,
        )
