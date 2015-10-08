from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# Applications

def get_applications():
    return Application.all()

def get_applications_by_status(status):
    return Application.filter(status__exact=status)

def get_pending_applications():
    return get_applications_by_status('Pending')

def get_applications_by_user(username):
    return Application.filter(user_submit__exact=username)

# Official Accounts

def get_official_accounts():
    return OfficialAccount.all()

# Admins

def add_admin(username, md5_password):
    try:
        Admin.create(username = username, password = md5_password)
        return True
    except IntegrityError:
        return False

def del_admin(username):
    try:
        admin = Admin.get(username = username)
        admin.delete()
        return True
    except ObjectDoesNotExist:
        return False

def get_admins():
    return Admin.all()
