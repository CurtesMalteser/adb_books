from flask import jsonify


def json_error(message, code):
    """
    A helper function for use with the @app.errorhandler(error) decorator to
    standardize error handling across the application.

    Each error handler should return a uniform JSON response with an appropriate
    message and status code.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
            Example response format:
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
    """

    return jsonify({
        "success": False,
        "error": code,
        "message": message,
        }), code