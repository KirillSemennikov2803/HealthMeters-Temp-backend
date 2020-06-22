import uuid
import datetime

import redis as redis

from general_module.models import Company, Licence
from main.response_processing import get_unauthorized_response, get_success_response


class InvalidData(Exception):
    def __init__(self, message):
        self.message = message


def validate_session():
    def request_dec(func):
        def request_handler(self, request):
            request_data = request.data
            if request_data.get("session") is None:
                return get_unauthorized_response()
            session = request_data["session"]
            if session_exists(session):
                return func(self, request)
            return get_unauthorized_response()
        return request_handler
    return request_dec


# Session must be validated before getting passed into this function.
def validate_licence():
    def request_dec(func):
        def request_handler(self, request):
            request_data = request.data
            session = request_data["session"]

            company = Company.objects.filter(guid=get_user(session))
            if not company:
                return get_unauthorized_response()

            company = company[0]
            now = datetime.datetime.utcnow()
            active_licence_exists =\
                Licence.objects.filter(company=company, start_date__lte=now, end_date__gte=now)\
                is not None

            if not active_licence_exists:
                return get_success_response({
                    "status": "error",
                    "reason": "licenceExpired"
                })

            return func(self, request)
        return request_handler
    return request_dec


""""""""""""""""""""""""""""""""""""""""""""""""
"    Warning:                                  "
"    This is an inner service and should not   "
"    be used inside the handlers!              "
""""""""""""""""""""""""""""""""""""""""""""""""


class SessionsStorage:
    sessions: redis.Redis

    def __init__(self):
        self.sessions = redis.Redis(host='localhost', port=6379, db=0)

    def is_session_attached(self, user: str):
        return bool(self.sessions.exists(str(user)))

    def attach_session(self, user: str, session):
        self.sessions.mset({str(user): str(session)})

    def delete_session(self, user: str):
        if not self.is_session_attached(user):
            return
        self.sessions.delete(str(user))

    def get_attached_session(self, user: str):
        if not self.is_session_attached(user):
            return None
        return self.sessions.get(str(user)).decode("utf-8")


""""""""""""""""""""""""""""""""""""""""""""""""
"    Warning:                                  "
"    This is an inner service and should not   "
"    be used inside the handlers!              "
""""""""""""""""""""""""""""""""""""""""""""""""


class UsersStorage:
    users_storage: redis.Redis

    def __init__(self):
        self.users_storage = redis.Redis(host='127.0.0.1', port=6379, db=1)

    def is_user_attached(self, session):
        return bool(self.users_storage.exists(str(session)))

    def attach_user(self, session: str, user: str):
        self.users_storage.mset({str(session): str(user)})

    def deattach_user(self, session: str):
        if not self.is_user_attached(session):
            return
        self.users_storage.delete(str(session))

    def get_attached_user(self, session):
        if not self.is_user_attached(session):
            return None
        return self.users_storage.get(str(session)).decode("utf-8")


""""""""""""""""""""""""""""""""""""""""""""""""
"    Use this functions inside the handlers    "
""""""""""""""""""""""""""""""""""""""""""""""""


def session_exists(session):
    users = UsersStorage()
    return users.is_user_attached(session)


def authorize_user(user: str, allow_multiple_sessions=False):
    sessions = SessionsStorage()
    users = UsersStorage()
    session = str(uuid.uuid4())

    if not allow_multiple_sessions and sessions.is_session_attached(user):
        # If the session for this user exists, we need to delete it
        # in order logout the user from the initial session and
        # rebind him to the newly created session:
        logout_user_full(user)

    if not user_authorized(user):
        users.attach_user(session, user)

    sessions.attach_session(user, session)
    return session


def user_authorized(user: str):
    sessions = SessionsStorage()
    return sessions.is_session_attached(user)


def logout_user(session: str):
    sessions = SessionsStorage()
    users = UsersStorage()
    sessions.delete_session(users.get_attached_user(session))
    users.deattach_user(session)


def logout_user_full(user: str):
    sessions = SessionsStorage()
    users = UsersStorage()

    while sessions.is_session_attached(user):
        users.deattach_user(sessions.get_attached_session(user))
        sessions.delete_session(user)


def get_user(session: str):
    return UsersStorage().get_attached_user(session)
