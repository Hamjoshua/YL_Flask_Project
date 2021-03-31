import datetime
from csv import reader
from requests import get

from flask import Flask, request, render_template, redirect, abort, session, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import abort, Api
from werkzeug.utils import secure_filename

from data import db_session
from data.__all_models import *
from forms.userform import UserForm
from forms.registerform import RegisterForm
from forms.loginform import LoginForm
from forms.topicform import TopicForm
from forms.messageform import MessageForm
from forms.searchtopicform import SearchTopicForm
from forms.questionform import QuestionForm
from forms.mapform import MapForm
from api import user_api
# from api import message_resources, subtopic_resources, \
#     topic_resources, user_resources

ROLES = ["user", "admin", "banned", "moder"]
MAX_TOPIC_SHOW = 20

TOPIC_IMG_DIR = 'static/img/topic_img'
PROFILE_IMG_DIR = 'static/img/profile_img'
QUESTION_IMG_DIR = 'static/img/quest_img'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I2D4423D2Q53D'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

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
    # Actions with cookies
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    if not visits_count:
        print('Вы пришли на эту страницу в первый раз за последние 2 года')

    return render_template(
        'index.html', title='WorldAnswerForum')


@app.route('/question', methods=['GET', 'POST'])
def user_question():
    form = QuestionForm()
    db_sess = db_session.create_session()
    if request.method == 'POST':
        if form.submit_question.data:
            question = Question()
            question.title = form.question_topic.data
            question.text = form.question_text.data
            question.email = form.email.data

            added_img = form.img.data
            if added_img:
                f = added_img
                filename = f'{QUESTION_IMG_DIR}/{f.filename}'
                f.save(filename)
                question.img = filename
            else:
                question.img = ''

            db_sess.add(question)
            db_sess.commit()
            return redirect('/')
    return render_template('question.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                'register.html', title='Регистрация', form=form,
                message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                'register.html', title='Регистрация', form=form,
                message="Такой email уже есть")
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.about = form.about.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)  # значение галочки
            return redirect("/")
        return render_template(
            'login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/profile/<int:user_id>')
def profile(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    return render_template(
        'user_profile.html', title='Профиль:', user=user)


@app.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    form = UserForm()
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if request.method == "GET":
        form.area.data = user.area
        form.about.data = user.about
        return render_template('user_edit.html', form=form, user=user)
    else:

        if form.edit_img.data:
            added_img = form.profile_img.data
            if added_img:
                f = added_img
                filename = f'{PROFILE_IMG_DIR}/{f.filename}'
                f.save(filename)
                user.profile_img = filename
            else:
                user.profile_img = ''

        user.area = form.area.data
        user.about = form.about.data
        db_sess.add(user)
        db_sess.commit()
        return redirect(f'/profile/{user.id}')


@app.route('/show_map/<int:user_id>', methods=['GET', 'POST'])
def show_map(user_id):
    form = MapForm()
    print(form.map_type.data)
    param = get(f'http://localhost:8000/api/users_param/{form.map_type.data}/{user_id}').json()
    return render_template('show_user_area.html', **param, form=form)


@app.route("/categories")
def all_categories():
    db_sess = db_session.create_session()
    categories = list(db_sess.query(Category).all())
    # divide by 4 columns
    four_category_lists = \
        [categories[len(categories) // 4 * i:len(categories) // 4 * (i + 1)]
         for i in range(4)]
    return render_template(
        "categories.html",
        four_category_lists=four_category_lists)


@app.route("/topics/<int:category_id>", methods=['GET', 'POST'])
def all_topics(category_id):
    form = SearchTopicForm()
    db_sess = db_session.create_session()
    if form.search.data is None:
        search_request = ''
    else:
        search_request = form.search.data
        category_id = int(form.category.data)
    form.category.process_data(category_id)

    if not category_id:
        topics = db_sess.query(Topic).filter(
            Topic.title.like(f'%{search_request}%'))
    else:
        topics = db_sess.query(Topic).filter(
            Topic.category_id == category_id,
            Topic.title.like(f'%{search_request}%'))

    topic_data = dict()
    for topic in topics:
        user = db_sess.query(User).filter(
            User.id == topic.author_id).first()
        category = db_sess.query(Category).filter(
            Category.id == topic.category_id).first()
        topic_data[topic] = dict()
        topic_data[topic]['user'] = user
        topic_data[topic]['category'] = category
        topic_data[topic]['len_message'] = \
            len(list(db_sess.query(Message).filter(
                Message.topic_id == topic.id)))
    return render_template(
        "topics.html", topics=topics, form=form,
        topic_data=topic_data)


@app.route('/topic/<int:topic_id>', methods=['GET', 'POST'])
def one_topic(topic_id):
    message_form = MessageForm()
    db_sess = db_session.create_session()
    topic = db_sess.query(Topic).get(topic_id)
    user = db_sess.query(User).get(topic.author_id)

    if request.method == 'POST':
        message = Message()
        message.message = message_form.message.data
        message.topic_id = topic.id
        message.author_id = current_user.id
        if current_user.id != user.id:
            notify = Notify()
            notify.user_id = user.id
            notify.href = f'/topic/{topic_id}'
            notify.text = \
                f'Пользователь {current_user.name} оставил комментарий под вашей темой!'
            db_sess.add(notify)
        db_sess.add(message)
        db_sess.commit()
        return redirect(f'/topic/{topic_id}')

    list_messages = list(db_sess.query(Message).filter(
        Message.topic_id == topic.id))
    messages_authors_dict = dict()
    for message in list_messages:
        messages_authors_dict[message] = \
            db_sess.query(User).filter(
                User.id == message.author_id).first()

    return render_template(
        'one_topic.html', topic=topic, user=user,
        messages_authors_dict=messages_authors_dict,
        messages=list_messages,
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
        topic.text = form.text.data

        added_img = form.img.data
        if added_img:
            f = added_img
            filename = f'{TOPIC_IMG_DIR}/{f.filename}'
            f.save(filename)
            topic.img = filename
        else:
            topic.img = ''

        topic.category_id = form.category.data
        topic.author_id = current_user.id
        db_sess.add(topic)
        db_sess.commit()
        return redirect(f'/topics/{form.category.data}')
    return render_template('topic_add.html', form=form)


'''
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
'''


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
            topic_id = message.topic_id
            return redirect(f'/topic/{topic_id}')
        else:
            abort(404)
    return render_template(
        'message_edit.html', form=form,
        message=message,
        topic=db_sess.query(Topic).get(
            message.topic_id))


@app.route('/message_delete/<int:message_id>', methods=['GET', 'POST'])
@login_required
def message_delete(message_id):
    db_sess = db_session.create_session()
    message = db_sess.query(Message).filter(
        Message.id == message_id).first()
    if message:
        topic_id = message.topic_id
        db_sess.delete(message)
        db_sess.commit()
        return redirect(f'/topic/{topic_id}')
    else:
        abort(404)


@app.route('/clear_notifies')
def clear_notifies():
    db_sess = db_session.create_session()
    notifies = db_sess.query(Notify).filter(
        Notify.user_id == current_user.id)
    for notify in notifies:
        db_sess.delete(notify)
    print(f'Уведомления {current_user.name} очищены')
    db_sess.commit()
    return redirect('/')


def get_notifies_num():
    db_sess = db_session.create_session()
    notifies = db_sess.query(Notify).filter(
        Notify.user_id == current_user.id)
    return len(list(notifies))


def init_category_table():
    db_sess = db_session.create_session()
    with open("static/categories.csv", mode='rt', encoding='utf-8') as csv_file:
        csv_file = [elem[0] for elem in reader(csv_file, delimiter=';')]
    for category_name in csv_file:
        category = db_sess.query(Category).filter(
            Category.title == category_name).first()
        if not category:
            category = Category()
            category.title = category_name
            db_sess.add(category)
            db_sess.commit()


def init_role_table():
    db_sess = db_session.create_session()
    for role_name in ROLES:
        role = db_sess.query(Role).filter(Role.role == role_name).first()
        if not role:
            role = Role()
            role.role = role_name
            db_sess.add(role)
            db_sess.commit()


def main():
    db_session.global_init('db/forum.db')
    init_role_table()
    init_category_table()
    app.jinja_env.globals.update(
        get_notifies_num=get_notifies_num)
    '''
    api.add_resource(message_resources.MessageResource, '/api/messages/<int:messages_id>')
    api.add_resource(message_resources.MessageListResource, '/api/messages')
    
    api.add_resource(subtopic_resources.SubtopicResource, '/api/subtopics/<int:subtopics_id>')
    api.add_resource(subtopic_resources.SubtopicListResource, '/api/subtopics')
    
    api.add_resource(topic_resources.TopicResource, '/api/topics/<int:topics_id>')
    api.add_resource(topic_resources.TopicListResource, '/api/topics')
    
    api.add_resource(user_resources.UserResource, '/api/users/<int:users_id>')
    api.add_resource(user_resources.UserListResource, '/api/users')
    '''
    app.register_blueprint(user_api.blueprint)
    app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
