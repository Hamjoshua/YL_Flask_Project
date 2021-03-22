import datetime
from requests import get

from flask import Flask, request, render_template, redirect, abort, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.__all_models import *
from forms.registerform import RegisterForm
from forms.loginform import LoginForm
from forms.topicform import TopicForm
from forms.subtopicform import SubtopicForm
from forms.messageform import MessageForm
from api.message_resources import *
from api.subtopic_resources import *
from api.topic_resources import *
from api.user_resources import *

ROLES = ["usual", "admin", "banned"]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I2D4423D2Q53D'

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)


def get_topics():
    db_sess = db_session.create_session()
    return db_sess.query(Topic).all()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Главная')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                'register.html', title='Регистрация', form=form,
                message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template(
                'register.html', title='Регистрация', form=form,
                message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)  # значение галочки
            return redirect("/")
        return render_template(
            'login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/topics")
def all_topics():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        topics = db_sess.query(Topic).all()
        return render_template("topics.html", topics=topics)
    return redirect("/login")


@app.route('/topic/<int:topic_id>')
def one_topic(topic_id):
    message_form = MessageForm()
    param = dict()
    db_sess = db_session.create_session()
    param['title'] = (db_sess.query(Topic).get(topic_id)).title
    param['topic_id'] = topic_id
    param['subtopics'] = db_sess.query(Subtopic).filter(
        Subtopic.topic_id == topic_id)
    dict_messages = dict()
    for st in param['subtopics']:
        dict_messages[st.id] = list((
            db_sess.query(Message).filter(
                Message.subtopic_id == st.id)))
    param['dict_messages'] = dict_messages
    return render_template('one_topic.html', **param,
                           form=message_form)


@app.route('/add_topic',  methods=['GET', 'POST'])
@login_required
def add_topics():
    form = TopicForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Topic).filter(Topic.title == form.title.data).first():
            return render_template(
                'topic_add.html', form=form,
                message="Такой топик уже есть")
        topic = Topic()
        topic.title = form.title.data
        topic.author_id = current_user.id
        db_sess.add(topic)
        db_sess.commit()
        return redirect('/topics')
    return render_template('topic_add.html', form=form)


@app.route('/topic_edit/<int:topic_id>', methods=['GET', 'POST'])
@login_required
def edit_topics(topic_id):
    form = TopicForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        topic = db_sess.query(Topic).filter(
            Topic.id == topic_id).first()
        if topic:
            form.title.data = topic.title
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        topic = db_sess.query(Topic).filter(
            Topic.id == topic_id).first()
        if topic:
            topic.title = form.title.data
            db_sess.add(topic)
            db_sess.commit()
            return redirect('/topics')
        else:
            abort(404)
    return render_template('topic_add.html', form=form)


@app.route('/topic_delete/<int:topic_id>', methods=['GET', 'POST'])
@login_required
def topics_delete(topic_id):
    db_sess = db_session.create_session()
    topic = db_sess.query(Topic).filter(Topic.id == topic_id).first()
    if topic:
        db_sess.delete(topic)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/topics')


@app.route('/add_subtopic/<int:topic_id>',  methods=['GET', 'POST'])
@login_required
def add_subtopics(topic_id):
    form = SubtopicForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Subtopic).filter(
                Subtopic.title == form.title.data).first():
            return render_template(
                'subtopic_add.html', form=form,
                message="Такой субтопик уже есть")
        topic = Subtopic()
        topic.title = form.title.data
        topic.author_id = int(current_user.id)
        topic.topic_id = int(topic_id)
        db_sess.add(topic)
        db_sess.commit()
        return redirect(f'/topic/{topic_id}')
    db_sess = db_session.create_session()
    return render_template(
        'subtopic_add.html', form=form,
        theme=db_sess.query(Topic).get(topic_id).title)


@app.route('/subtopic_edit/<int:subtopic_id>', methods=['GET', 'POST'])
@login_required
def edit_subtopics(subtopic_id):
    form = SubtopicForm()
    db_sess = db_session.create_session()
    subtopic = db_sess.query(Subtopic).filter(
        Subtopic.id == subtopic_id).first()
    if request.method == "GET":
        if subtopic:
            form.title.data = subtopic.title
        else:
            abort(404)
    if form.validate_on_submit():
        if subtopic:
            subtopic.title = form.title.data
            db_sess.add(subtopic)
            db_sess.commit()
            return redirect(f'/topic/{subtopic.topic_id}')
        else:
            abort(404)
    return render_template(
        'subtopic_add.html', form=form,
        theme=db_sess.query(Topic).get(subtopic.topic_id).title)


@app.route('/subtopic_delete/<int:subtopic_id>', methods=['GET', 'POST'])
@login_required
def subtopics_delete(subtopic_id):
    db_sess = db_session.create_session()
    subtopic = db_sess.query(Subtopic).filter(
        Subtopic.id == subtopic_id).first()
    if subtopic:
        topic_id = subtopic.topic_id
        db_sess.delete(subtopic)
        db_sess.commit()
        return redirect(f'/topic/{topic_id}')
    else:
        abort(404)


@app.route('/message_edit/<int:message_id>', methods=['GET', 'POST'])
@login_required
def edit_message(message_id):
    form = MessageForm()
    db_sess = db_session.create_session()
    message = db_sess.query(Message).filter(
        Message.id == message_id).first()
    if request.method == "GET":
        if message:
            form.message.data = message.message
        else:
            abort(404)
    if form.validate_on_submit():
        if message:
            message.message = form.message.data
            db_sess.add(message)
            db_sess.commit()
            topic_id = db_sess.query(Topic).get(
                db_sess.query(Subtopic).get(
                    message.subtopic_id).topic_id).id
            return redirect(f'/topic/{topic_id}')
        else:
            abort(404)
    return render_template(
        'message_edit.html', form=form,
        theme=db_sess.query(Topic).get(
            db_sess.query(Subtopic).get(
                message.subtopic_id).topic_id).title)


@app.route('/message_delete/<int:message_id>', methods=['GET', 'POST'])
@login_required
def message_delete(message_id):
    db_sess = db_session.create_session()
    message = db_sess.query(Message).filter(
        Message.id == message_id).first()
    if message:
        topic_id = db_sess.query(Topic).get(
            db_sess.query(Subtopic).get(
                message.subtopic_id).topic_id).id
        db_sess.delete(message)
        db_sess.commit()
        return redirect(f'/topic/{topic_id}')
    else:
        abort(404)


@app.route('/subtopic/<int:subtopic_id>', methods=['GET', 'POST'])
def one_subtopic(subtopic_id):
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


def main():
    db_session.global_init('db/forum.db')

    api.add_resource(message_resources.MessageResource, '/api/messages/<int:messages_id>')
    api.add_resource(message_resources.MessageListResource, '/api/messages')
    
    api.add_resource(subtopic_resources.SubtopicResource, '/api/subtopics/<int:subtopics_id>')
    api.add_resource(subtopic_resources.SubtopicListResource, '/api/subtopics')
    
    api.add_resource(topic_resources.TopicResource, '/api/topics/<int:topics_id>')
    api.add_resource(topic_resources.TopicListResource, '/api/topics')
    
    api.add_resource(user_resources.UserResource, '/api/users/<int:users_id>')
    api.add_resource(user_resources.UserListResource, '/api/users')

    app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
