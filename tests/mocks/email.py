class Error:
    """Class that holds the error objects accepted by python-http-client exceptions"""
    code = None
    reason = None
    hdrs = None

    def read(self):
        pass
