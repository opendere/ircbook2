from ircbook import models
from ircbook.config import get_session
from ircbook.privileges import assert_admin


def register_user(account_name):
    new_user = models.User(account_name=account_name)
    get_session().add(new_user)
    get_session().commit()
    return new_user


def confirm_user(admin_name, account_name):
    assert_admin(admin_name)

    affected_user = get_session().query(models.User).filter(models.User.account_name == account_name).one()
    affected_user.is_confirmed = True
    get_session().commit()
    return True


def admin_user(admin_name, account_name):
    assert_admin(admin_name)

    affected_user = get_session().query(models.User).filter(models.User.account_name == account_name).one()
    affected_user.is_admin = True
    get_session().commit()
    return True


def get_usernames(is_confirmed=None, is_admin=None):
    res = get_session().query(models.User.account_name)
    if is_confirmed is not None:
        res = res.filter(models.User.is_confirmed == is_confirmed)
    if is_admin is not None:
        res = res.filter(models.User.is_admin == is_admin)
    return [r for r, in res]
