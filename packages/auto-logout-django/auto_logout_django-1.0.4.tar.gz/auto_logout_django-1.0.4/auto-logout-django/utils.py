from datetime import timedelta, datetime
from typing import Union
from django.http import HttpRequest
from django.utils import timezone

def seconds_until_session_end(
    request: HttpRequest,
    session_time: Union[int, timedelta],
    current_time: datetime = None
) -> float:
    if current_time is None:
        current_time = timezone.now()

    if isinstance(session_time, timedelta):
        ttl = session_time
    elif isinstance(session_time, int):
        ttl = timedelta(seconds=session_time)
    else:
        raise TypeError(f"AUTO_LOGOUT['SESSION_TIME'] should be `int` or `timedelta`, "
                        f"not `{type(session_time).__name__}`.")

    last_login = request.user.last_login
    if last_login is None:
        return 0.0

    return (last_login + ttl - current_time).total_seconds()

def seconds_until_idle_time_end(
    request: HttpRequest,
    idle_time: Union[int, timedelta],
    current_time: datetime = None
) -> float:
    if current_time is None:
        current_time = timezone.now()

    if isinstance(idle_time, timedelta):
        ttl = idle_time
    elif isinstance(idle_time, int):
        ttl = timedelta(seconds=idle_time)
    else:
        raise TypeError(f"AUTO_LOGOUT['IDLE_TIME'] should be `int` or `timedelta`, "
                        f"not `{type(idle_time).__name__}`.")

    last_request_time = request.session.get('django_auto_logout_last_request')
    if last_request_time is None:
        return ttl.total_seconds()

    last_request_time = datetime.fromisoformat(last_request_time)
    return (last_request_time + ttl - current_time).total_seconds()