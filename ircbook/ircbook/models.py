from ircbook import config
import datetime as dt
from sqlalchemy import Table, Column, Integer, BigInteger, DateTime, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Action(Base):
    # Action is immutable, reproducable
    __tablename__ = "action"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=dt.datetime.utcnow)
    params = Column(String)  # semicolon-separated action parameters


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint('account_name', name='unique_account_name'),
    )

    id = Column(Integer, primary_key=True)

    account_name = Column(String)
    create_timestamp = Column(DateTime, default=dt.datetime.utcnow)

    is_confirmed = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    cash = Column(BigInteger, default=int(1e8))  # 1,000,000 ircbucks * 100 cents
    net_demurrage = Column(Integer, default=0)
    positions = relationship("NetPosition")
    orders = relationship("Order")


class Claim(Base):
    __tablename__ = "claim"
    symbol = Column(String, primary_key=True)
    is_approved = Column(Boolean, default=False)
    create_timestamp = Column(DateTime, default=dt.datetime.utcnow)
    expire_timestamp = Column(DateTime)
    terms = Column(String)
    judgements = relationship("Judgement")


class Judgement(Base):
      # leaving open ended in case we want more than one judge
    __tablename__ = "judgement"
    claim_symbol = Column(String, ForeignKey('claim.symbol'), primary_key=True)
    claim = relationship("Claim")
    timestamp = Column(DateTime, default=dt.datetime.utcnow)
    judge_user_id = Column(Integer, ForeignKey('user.id'))
    judge = relationship("User")
    is_yes = Column(Boolean, nullable=True)


class Trade(Base):
    __tablename__ = "trade"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=dt.datetime.utcnow)

    buy_user_id = Column(Integer, ForeignKey('user.id'))
    buy_user = relationship("User", foreign_keys=[buy_user_id])

    sell_user_id = Column(Integer, ForeignKey('user.id'))
    sell_user = relationship("User", foreign_keys=[sell_user_id])

    buy_order_id = Column(Integer, ForeignKey('order.id'))
    buy_order = relationship("Order", foreign_keys=[buy_order_id])

    sell_order_id = Column(Integer, ForeignKey('order.id'))
    sell_order = relationship("Order", foreign_keys=[sell_order_id])

    quantity = Column(Integer)
    price = Column(Integer)


class PositionQueueItem(Base):
    """
    FIFO queue of positions
    If a long user sells coupons to reduce their position, they're effectively selling off positions from this queue
    This system of account is designed to handle demurrage of open positions
    """
    __tablename__ = "positionqueueitem"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('netposition.user_id'))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    claim_id = Column(String, ForeignKey('claim.symbol'))
    claim = relationship("Claim")

    timestamp = Column(DateTime)
    price = Column(Integer)
    net_quantity = Column(Integer)  # Users should never have both long (positive) and short (negative) positions in their queue


class NetPosition(Base):
    __tablename__ = "netposition"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    user = relationship("User")

    claim_id = Column(String, ForeignKey('claim.symbol'))
    claim = relationship("Claim")

    net_quantity = Column(Integer)

    # for position demurrage
    position_queue = relationship("PositionQueueItem")
    position_queue = relationship("PositionQueueItem")


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=dt.datetime.utcnow)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    claim_id = Column(String, ForeignKey('claim.symbol'))
    claim = relationship("Claim")

    is_buy = Column(Boolean)
    price = Column(Integer)
    quantity = Column(Integer)


#Base.metadata.create_all(config.get_engine())
