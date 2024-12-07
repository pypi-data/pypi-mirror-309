import requests
import threading
import sys
import time
import traceback

_local_sessions = threading.local()

def get_session_data():
    if not hasattr(_local_sessions, "session"):
        _local_sessions.session = (requests.Session(), 0)

    session, counter = _local_sessions.session
    counter += 1
    _local_sessions.session = (session, counter)

    return session, counter

def make_request_wrapper(endpoint, method, params, request_cb):
    for sleep_time in [1, 5, 30, 60, None]:
        try:
            return request_cb(endpoint, method, params)
        except Exception as e:
            last_error = e
            print(f"Error [{repr(e)}] and sleep for {sleep_time}", file=sys.stderr)
            traceback.print_exc()
            if sleep_time is None:
                raise e
            time.sleep(sleep_time)
    raise Exception("Unknown error")