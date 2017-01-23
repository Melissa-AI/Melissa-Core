from melissa import profile
from pushbullet import Pushbullet


def handle_exceptions(f):  # pragma: no cover
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print("Error: ", e)
    return inner


@handle_exceptions
def push(info):
    pb = Pushbullet(profile.data['push_bullet'])
    pb.push_note(profile.data['va_name'], info)  # Send Notification
