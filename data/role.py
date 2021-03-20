from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

import sqlalchemy


class Role(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'roles'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    role = sqlalchemy.Column(sqlalchemy.String)  # будет три роли: "usual", "admin", "banned"
