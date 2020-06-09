from general_module.models import User
import uuid


def generate_user_guid():
    for i in range(0, 20, 1):
        guid = str(uuid.uuid4())
        user = User.objects.filter(guid=guid)

        if user:
            continue

        return guid

    raise SystemError

