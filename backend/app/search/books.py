import os
from flask import (
    request,
    jsonify,
    abort,
)
import requests
from requests import (
    JSONDecodeError,
    RequestException,
)

from app.config import (
    SEARCH_ENDPOINT,
    DEFAULT_PAGE,
    DEFAULT_LIMIT,
)
from app.exceptions.invalid_request_error import InvalidRequestError

api_key = os.environ.get('ISBNDB_KEY')

def books(user_agent):
    query = request.args.get('q')
    page = request.args.get('page', default=DEFAULT_PAGE)
    limit = request.args.get('limit', default=DEFAULT_LIMIT)

    if not query:
        raise  InvalidRequestError(message="Missing 'q' parameter", code=400)

    url = f'{SEARCH_ENDPOINT}/{query}?page={page}&pageSize={limit}'

    headers = {
        "User-Agent": user_agent,
        "Authorization": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())  # Flask's jsonify adds the correct content type headers automatically

    except JSONDecodeError:
        abort(500, description="Invalid JSON response from upstream server.")

    except RequestException as e:
        abort(500, description=f"An error occurred while fetching data: {str(e)}")