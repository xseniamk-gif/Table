'''id
title (String)
chief (Integer)
members (list of id`s)
email (String)'''
import datetime
import sqlalchemy
from sqlalchemy.util.preloaded import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Department(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey('users.id'),
                              nullable=True)

    # Для SQLite используем JSON (он работает как текст)
    members = sqlalchemy.Column(sqlalchemy.JSON, default=list)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)

    user = orm.relationship('User')