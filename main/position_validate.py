from general_module.models import Employee


def validate_admin_site_add_delete(role: str, user: Employee):
    if user.role == "full_admin":
        return True
    if user.role == "admin" and role != "admin":
        return True
    return False


def validate_attach_admin(manger: Employee, worker: Employee):
    if manger.role == "manager":
        if worker.role == "worker":
            return True
    return False


def validate_company_context_attach(admin: Employee, manage: Employee, worker: Employee):
    return admin.company == manage.company == worker.company
