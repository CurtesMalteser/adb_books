from flask import (
    request,
    jsonify,
    abort,
)
import requests
from requests.exceptions import (
    JSONDecodeError,
    RequestException,
)
from app.exceptions.invalid_request_error import InvalidRequestError


def books(base_url, user_agent):
    query = request.args.get('q')

    if not query:
        raise  InvalidRequestError(message="Missing 'q' parameter", code=400)


    url = f'{base_url}/search.json?q={query}'
    headers = {
        "User-Agent": f'{user_agent}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())  # Flask's jsonify adds the correct content type headers automatically

    except JSONDecodeError:
        abort(500, description="Invalid JSON response from upstream server.")

    except RequestException as e:
        abort(500, description=f"An error occurred while fetching data: {str(e)}")