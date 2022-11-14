REQUEST = (2, "Request failed")

class CoziException(Exception):
    """Class to throw general exception."""

    def __init__(self, error, details=None):
        """Initialize CoziException."""
        # Call the base class constructor with the parameters it needs
        super(CoziException, self).__init__(error[1])

        self.errcode = error[0]
        self.message = error[1]
        self.details = details

class InvalidLoginException(CoziException):
    """Class to throw login exception."""

class RequestException(CoziException):
    """Class to throw request exception."""