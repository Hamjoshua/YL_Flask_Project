from flask import render_template, Flask, request, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from data import db_session
from data.user import User
from data.role import Role
from data.topic import Topic
from data.message import Message, MessageForm
from data.subtopic import Subtopic

app = Flask(__name__)
app.config['SECRET_KEY'] = 'IDDQD'
login_manager = LoginManager()
login_manager.init_app(app)


def get_topics():
    return db_session.create_session().query(Topic).all()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная', topics=get_topics())


@app.route('/topic/<int:topic_id>')
def topic_id(topic_id):
    db_sess = db_session.create_session()
    subtopics = db_sess.query(Subtopic).filter(Subtopic.topic_id == topic_id)
    topic_title = (db_sess.query(Topic).get(topic_id)).title
    first_messages = []
    for st in subtopics:
        first_messages.append((db_sess.query(Message).filter(Message.subtopic_id == st.id))[0])
    return render_template('topic_id.html', title=f'Содержание темы {topic_title}',
                           topics=get_topics(), subtopics=subtopics, messages=first_messages)


@app.route('/subtopic/<int:subtopic_id>', methods=['GET', 'POST'])
def subtopic_id(subtopic_id):
    form = MessageForm()

    db_sess = db_session.create_session()
    if form.validate_on_submit():
        new_msg = Message(
            message=form.data['message'],
            subtopic_id=subtopic_id,
            author_id=current_user.id
        )
        db_sess.add(new_msg)
        db_sess.commit()

    messages = db_sess.query(Message).all()
    subtopic_title = messages[0].subtopic.title

    return render_template('subtopic_id.html', title=subtopic_title, topics=get_topics(),
                           messages=messages, form=form)


if __name__ == '__main__':
    db_session.global_init('db/forum.db')
    import datetime

    app.run()
