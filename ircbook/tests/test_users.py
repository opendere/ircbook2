from ircbook import users


def test_register_user():
    user = users.register_user('a')
    assert user.is_confirmed == False
    assert user.cash == 1e8
    assert user.net_demurrage == 0
    assert user.positions == []
    assert user.orders == []


def test_get_usernames():
    assert users.get_usernames() == []

    user_a = users.register_user('a')
    user_b = users.register_user('b')
    user_c = users.register_user('c')

    assert users.get_usernames() == ['a', 'b', 'c']

    user_a.is_admin = True
    user_c.is_admin = True
    assert users.get_usernames(is_admin=True) == ['a', 'c']


def test_confirm_user():
    users.register_user('reguser')
    user_b = users.register_user('admin')

    assert not users.confirm_user('admin', 'reguser')

    user_b.is_admin = True

    assert users.confirm_user('admin', 'reguser')
