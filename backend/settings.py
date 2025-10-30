import os
import time
from environs import Env
from loguru import logger


os.environ['TZ'] = 'Asia/Ho_Chi_Minh'
time.tzset()


log_file_format = "{time:YYYY-MM-DD}.log"
logger.add(f"logging/{log_file_format}", rotation="00:00", retention="7 days", enqueue=True)


env = Env()
logger.info(f"Loading environment variables...")


FASTAPI_ENVIRONMENT = env.str("FASTAPI_ENVIRONMENT", default="PRODUCTION")
SERVER_IP = env.str("SERVER_IP", default="0.0.0.0")
SERVER_PORT = env.int("SERVER_PORT", default=5000)


ISSUER_NAME = env.str("ISSUER_NAME")


RESET_PASSWORD_EXPIRED_MINUTES = env.int("RESET_PASSWORD_EXPIRED_MINUTES")


JWT_SECRET = env.str("JWT_SECRET")
JWT_ALGORITHM = env.str("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int("ACCESS_TOKEN_EXPIRE_MINUTES")
OTP_EXPIRE_MINUTES = env.int("OTP_EXPIRE_MINUTES")


POSTGRES_HOST = env.str("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_USER = env.str("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD", default="postgres")
POSTGRES_DB = env.str("POSTGRES_DB", default="postgres")
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
SQLALCHEMY_DATABASE_URL = env.str("SQLALCHEMY_DATABASE_URL", default=SQLALCHEMY_DATABASE_URL)


logger.info(f">>> POSTGRES_USER = {POSTGRES_USER}")


SMTP_HOST = env.str("SMTP_HOST", default="mailhog")
SMTP_PORT = env.int("SMTP_PORT", default=1025)
SMTP_GUI_PORT = env.int("SMTP_GUI_PORT", default=8025)
SMTP_TLS = env.bool("SMTP_TLS", default=False)
SMTP_SSL = env.bool("SMTP_SSL", default=False)
SMTP_USER = env.str("SMTP_USER", default="")
SMTP_PASSWORD = env.str("SMTP_PASSWORD", default="")
EMAILS_FROM_NAME = env.str("EMAILS_FROM_NAME", default="Vũ Văn Nghĩa - Authenticator")
EMAILS_FROM_EMAIL = env.str("EMAILS_FROM_EMAIL", default="no-reply.vu.van.nghia@mailhog.com")


ADMIN_DEFAULT_NAME = env.str("ADMIN_DEFAULT_NAME", default="admin_name")
ADMIN_DEFAULT_AGE = env.int("ADMIN_DEFAULT_AGE", default=20)
ADMIN_DEFAULT_USERNAME = env.str("ADMIN_DEFAULT_USERNAME", default="admin_username")
ADMIN_DEFAULT_PASSWORD = env.str("ADMIN_DEFAULT_PASSWORD", default="admin_password")
ADMIN_DEFAULT_EMAIL = env.str("ADMIN_DEFAULT_EMAIL", default="admin_email")
