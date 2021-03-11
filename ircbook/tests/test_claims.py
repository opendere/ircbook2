import pytest
from ircbook import users, claims
import datetime as dt


def test_create_claim():
    claim = claims.create_claim(
        'all_tests_pass',
        dt.date(2025, 1, 1),
        'all ircbook tests pass',
    )
    assert claim.is_approved == False
    assert claim.symbol == 'all_tests_pass'
    assert claim.terms == 'all ircbook tests pass'
    assert claim.create_timestamp.date() == dt.date.today()
    assert claim.expire_timestamp == dt.datetime(2025, 1, 1)
    assert claim.judgements == []


def test_approve_claim_not_admin():
    user_a = users.register_user('a')
    claims.create_claim(
        'all_tests_pass',
        dt.date(2025, 1, 1),
        'all ircbook tests pass',
    )
    with pytest.raises(Exception):
        claims.approve_claim('a', 'all_tests_pass')


def test_approve_claim():
    admin_user_a = users.register_user('a')
    admin_user_a.is_admin = True
    claim = claims.create_claim(
        'all_tests_pass',
        dt.date(2025, 1, 1),
        'all ircbook tests pass',
    )
    claims.approve_claim('a', 'all_tests_pass')
    assert claim.is_approved



def test_judge_claim_not_admin():
    user_a = users.register_user('a')
    claims.create_claim(
        'all_tests_pass',
        dt.date(2025, 1, 1),
        'all ircbook tests pass',
    )
    with pytest.raises(Exception):
        claims.judge_claim('a', 'all_tests_pass', True)



def test_judge_claim():
    assert claims.get_claim_judgement('all_tests_pass') == None
    admin_user_a = users.register_user('a')
    admin_user_a.is_admin = True
    claims.create_claim(
        'all_tests_pass',
        dt.date(2025, 1, 1),
        'all ircbook tests pass',
    )
    claims.judge_claim('a', 'all_tests_pass', False)
    assert claims.get_claim_judgement('all_tests_pass') == False


def test_judge_claim_twice():
    admin_user_a = users.register_user('a')
    admin_user_a.is_admin = True
    admin_user_b = users.register_user('b')
    admin_user_b.is_admin = True
    claims.create_claim(
        'all_tests_pass',
        dt.date(2025, 1, 1),
        'all ircbook tests pass',
    )
    claims.judge_claim('a', 'all_tests_pass', False)
    with pytest.raises(Exception):
        claims.judge_claim('b', 'all_tests_pass', False)
