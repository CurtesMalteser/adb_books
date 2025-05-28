"""
Custom exception used to represent expected request errors with a specific HTTP status code.

`InvalidRequestError` improves developer experience by centralizing error handling.
Instead of calling `abort(...)` throughout the codebase, this exception can be raised
with a custom message and status code, which is then handled cleanly by a registered
Flask error handler.

Example usage with Flask:

    @app.errorhandler(InvalidRequestError)
    def handle_invalid_request(error):
        return json_error(error.message, error.code)
"""


class InvalidRequestError(Exception):
    """Custom exception for invalid requests with a specific HTTP status code."""

    def __init__(self, code, message):
        """Init the exception with a status code and message."""
        self.message = message
        self.code = code
        super().__init__(self.message)
