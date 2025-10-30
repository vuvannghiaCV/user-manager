import settings
import emails
from loguru import logger


async def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    """
    Send an email to the given address with the given subject and HTML content.

    Args:
        email_to (str): The email address to send to.
        subject (str, optional): The subject of the email. Defaults to "".
        html_content (str, optional): The HTML content of the email. Defaults to "".
    """

    logger.info(f"Send email to {email_to} with subject {subject}")

    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(
            settings.EMAILS_FROM_NAME,
            settings.EMAILS_FROM_EMAIL
        ),
    )
    smtp_options = {
        "host": settings.SMTP_HOST,
        "port": settings.SMTP_PORT
    }

    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD

    message.send(to=email_to, smtp=smtp_options)
