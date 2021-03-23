from functools import wraps
from typing import List

from flask import (
    flash,
    redirect,
    request,
    session,
    url_for,
)


def camel_case_to_title_case(elements: List[str]) -> List[str]:
    """Return a list of camel cased words as splitted title case.

    e.g.: newWorld -> New World
    """
    new_elements = []
    for word in elements:
        new_word = ""
        for idx, letter in enumerate(word):
            if letter.isupper():
                new_word += " " + letter
            elif idx == 0:
                new_word += letter.title()
            else:
                new_word += letter
        new_elements.append(new_word)
    return new_elements


def is_ajax(request):
    """Determine if a request is ajax."""
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def ensure_api_key(func):
    """Decorator to ensure that the api_key exists in the session when a
    protected endpoint is called.
    """
    print('x')
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("api_key") is None:
            flash(
                "No api key is found in session. Please enter your api key "
                "to continue."
            )
            if is_ajax(request):
                return {"redirect": url_for("api.register_api_key")}, 403
            else:
                return redirect(url_for("api.register_api_key"))
        return func(*args, **kwargs)

    return wrapper
