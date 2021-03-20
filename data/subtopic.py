from .db_session import SqlAlchemyBase
from sqlalchemy import orm
import sqlalchemy

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

from sqlalchemy_serializer import SerializerMixin


class CreateSubtopic(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    topic_id = SelectField('Тема', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Готово')


class Subtopic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'subtopics'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('topics.id'),
                                  nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'),
                                  nullable=False)

    user = orm.relation('User')
    topic = orm.relation('Topic')

    def __repr__(self):
        return f'<Subtopic> {self.title} {self.topic_id} {self.author_id}'
