from sqlalchemy import Column, Integer, String

from sun.db import db
from sun.db.operators import get_filters_expr

DB_URI = 'sqlite:///:memory:'


def test_db_operators_fetch_rows():
    db.connect(DB_URI)

    class User(db.BaseModel):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        username = Column(String(50), default='')
        age = Column(Integer)

    class Book(db.BaseModel):
        __tablename__ = "books"
        id = Column(Integer, primary_key=True)
        title = Column(String(20), index=True)

    db.create_all()
    lucy = User.create(**{
        'username': 'Lucy',
        'age': 13,
    })
    jack = User.create(**{
        'username': 'Jack',
        'age': 20,
    })
    groot = User.create(**{
        'username': 'Groot',
        'age': 32,
    })

    assert lucy.id > 0

    users = User.query().filter(User.username.like('%c%'), User.age > 0).all()
    assert len(
        users
    ) == 2, 'Fetch users count in common way should work properly'

    filters = {
        'username__like': '%c%',
        'age__gt': 0,
    }
    users = User.query().filter(*get_filters_expr(User, **filters)).all()
    assert len(users) == 2
