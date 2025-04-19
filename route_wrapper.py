from functools import wraps

from flask import redirect, session


def prof_login_required(f):
    """
    This decorator ensures that a user is logged in before accessing certain routes.
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if "professor" in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")

    return wrap


def student_login_required(f):
    """
    This decorator ensures that a user is logged in before accessing certain routes.
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if "student" in session:
            return f(*args, **kwargs)
        else:
            return redirect("/")

    return wrap
