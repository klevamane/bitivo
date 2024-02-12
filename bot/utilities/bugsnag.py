import bugsnag


def post_bugsnag_exception(exception, message):
    """Method that raises exceptions on the slack bot
        Args:
            exception: exception raised
            message(str): message mapped to the exception
    """
    bugsnag.notify(exception, extra_fields={'message': message})
