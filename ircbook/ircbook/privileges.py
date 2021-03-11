from ircbook.config import get_session
from ircbook import models


def assert_admin(account_name):
    admin = get_session().query(models.User)\
                    .filter(models.User.account_name == account_name)\
                    .filter(models.User.is_admin)\
                    .first()
    if not admin:
        raise Exception('invalid permissions')
    return admin
