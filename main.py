from flask import Flask
from data import db_session
from data.users import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
user1 = ["Scott", "Ridley", 21, "captain", "research engineer", "module_1", "scott_chief@mars.org"]
user2 = ["kuzbuk", "kuzbukov", 24, "lox", "klown", "v_kosmose", "salam@mars.org"]
user3 = ["abdul", "abdulov", 13, "lox", "klown", "xz", "net@mars.org"]
my_users = [user1, user2, user3]


def create_user(db_sess, params):
    user = User()
    user.surname = params[0]
    user.name = params[1]
    user.age = params[2]
    user.position = params[3]
    user.speciality = params[4]
    user.address = params[5]
    user.email = params[6]
    db_sess.add(user)
    db_sess.commit()


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    for u in my_users:
        create_user(db_sess, u)
    app.run()


if __name__ == '__main__':
    main()