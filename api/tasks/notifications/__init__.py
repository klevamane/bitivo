# Utilities
# app config
from config import AppConfig

from ...utilities.emails.email_factories.send_email_builder import build_email_sender

SendEmail = build_email_sender(AppConfig.MAIL_SERVICE)
