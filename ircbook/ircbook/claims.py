from ircbook import models
from ircbook.config import get_session
from ircbook.privileges import assert_admin
from ircbook.collateral import _claim_settlement_hook


def create_claim(symbol, date, terms):
    new_claim = models.Claim(
        symbol=symbol,
        expire_timestamp=date,
        terms=terms
    )
    get_session().add(new_claim)
    get_session().commit()
    return new_claim


def approve_claim(admin_account, symbol):
    assert_admin(admin_account)

    affected_claim = get_session().query(models.Claim).filter(models.Claim.symbol == symbol).one()
    affected_claim.is_approved = True
    get_session().commit()
    return True


def judge_claim(admin_account, symbol, is_yes):
    admin = assert_admin(admin_account)

    judgement = get_session().query(models.Judgement).filter(models.Judgement.claim_symbol == symbol).first()
    if judgement is None:
        judgement = models.Judgement(
            claim_symbol=symbol,
            judge=admin,
            is_yes=is_yes
        )
        get_session().add(judgement)
        get_session().commit()
    else:
        # for now we don't require a majority, just first to judge judges
        raise Exception('claim already judged')

    _claim_settlement_hook(symbol)
    return judgement


def get_claim_judgement(symbol):
    res = get_session().query(models.Judgement.is_yes).filter(models.Judgement.claim_symbol == symbol).first()
    if isinstance(res, tuple):
        res, = res
    return res
