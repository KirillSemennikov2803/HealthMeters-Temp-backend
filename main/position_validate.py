from user_service.models import User


def validate_admin_site_add_delete(role: str, user: User):
    if user.position == "full_admin":
        return True
    if user.position == "admin" and role != "admin":
        return True
    return False


def validate_attach_admin(manger: User, worker: User):
    if manger.position == "manager":
        if worker.position == "worker":
            return True
    return False


def validate_company_context_attach(admin: User, manage: User, worker: User):
    return admin.company == manage.company == worker.company
