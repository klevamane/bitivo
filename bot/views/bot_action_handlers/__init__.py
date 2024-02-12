"""Module to handle bot action handlers"""

from .spreadsheet_handlers import SpreadsheetHandlers
from .response_handlers import ResponseHandlers
from .request_handlers import RequestHandlers
from .notification_handlers import NotificationHandlers
from .cancel_handlers import CancelHandlers


class BotActionHandlers(
        SpreadsheetHandlers,
        ResponseHandlers,
        RequestHandlers,
        NotificationHandlers,
        CancelHandlers,):
    pass
