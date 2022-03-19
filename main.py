from flask import Flask
from flask import jsonify
from data import db_session
from data.users import User
from data.Jobs import Jobs
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.login import LoginForm
from flask import render_template, redirect
from datetime import datetime
from forms.register import RegisterForm
from moduls import jobs_api
from flask import make_response



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def create_user(db_sess, params):
    user = User()
    user.surname = params[0]
    user.name = params[1]
    user.age = params[2]
    user.position = params[3]
    user.speciality = params[4]
    user.address = params[5]
    user.email = params[6]
    user.set_password(params[7])
    db_sess.add(user)
    db_sess.commit()
    return user



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.is_finished != True)
    return render_template("index.html", jobs=jobs)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            email=form.email.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():

    db_session.global_init("db/list_jobs.db")
    db_sess = db_session.create_session()
    user1 = ["Scott", "Ridley20", 21, "captain", "research engineer", "module_1", "scott_chief@mars.org", "a"]
    user2 = ["kuzbuk", "kuzbukov", 24, "lox", "klown", "v_kosmose", "salam@mars.org", "a"]
    user3 = ["abdul", "abdulov", 13, "lox", "klown", "xz", "net@mars.org", "a"]
    my_users = [user1, user2, user3]
    for u in my_users:
        create_user(db_sess, u)
    job = Jobs(team_leader=1, job="Первая работа", collaborators='1,2',
               work_size=2, start_date=datetime.now(), end_date=datetime.now(),
               is_finished=False)
    db_sess.add(job)
    db_sess.commit()
    app.register_blueprint(jobs_api.blueprint)
    app.run()




if __name__ == '__main__':
    main()