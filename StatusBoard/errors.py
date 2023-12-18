from werkzeug.exceptions import HTTPException
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return "We broke some stuff...sorry about that", 500