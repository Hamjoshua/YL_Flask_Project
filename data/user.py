from .db_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

from flask_wtf import FlaskForm

from wtforms import PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField('Псевдоним', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня', validators=[DataRequired()])
    submit = SubmitField('Готово')


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    role_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('roles.id'), default=1)

    role = orm.relation('Role')

    def __repr__(self):
        return f'<User> {self.name} {self.role}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
