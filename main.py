from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask import Flask, render_template, redirect, make_response, jsonify, request, abort
from sqlalchemy.orm.collections import collection

import app
from data import db_session, jobs_api
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from forms.jobsForm import JobsForm
from forms.login import RegisterForm

from forms.loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def init_data_users():
    session = db_session.create_session()
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.set_password("cap")

    user1 = User(
        surname="Las",
        name="Parker",
        age=23,
        position="medic",
        speciality="research engineer",
        address="module_1",
        email="las@mars.org")
    user1.set_password("123")

    user2 = User(
        surname="Sco",
        name="Dley",
        age=21,
        position="rid",
        speciality="research engineer",
        address="module_1",
        email="ssssf@mars.org")
    user2.set_password("123")

    user3 = User(
        surname="Scott",
        name="Ridley",
        age=21,
        position="captain",
        speciality="research engineer",
        address="module_1",
        email="sc@mars.org")
    user3.set_password("123")

    user4 = User(
        surname="Jon",
        name="Mirfy",
        age=25,
        position="energying",
        speciality="engineer",
        address="module_1",
        email="ku@mars.org")
    user4.set_password("123")

    user5 = User(
        surname="Sanders",
        name="Teddy",
        age=28,
        position="geologist",
        speciality="geology",
        address="module_1",
        email="sanders@mars.org")
    user5.set_password("123")

    session.add(user)
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.add(user4)
    session.add(user5)
    session.commit()


def init_data_jobs():
    db_sess = db_session.create_session()
    job1 = Jobs(team_leader=1, job='deployment of residential modules 1 and 2',
                work_size=15, is_finished=False, collaborators='2')
    job2 = Jobs(team_leader=2, job='maintenance of residential modules',
                work_size=10, is_finished=False, collaborators='1')
    job3 = Jobs(team_leader=3, job='research work',
                work_size=20, is_finished=False, collaborators='3')
    job4 = Jobs(team_leader=4, job='geological survey',
                work_size=12, is_finished=True, collaborators='4,5')
    job5 = Jobs(team_leader=5, job='soil analysis',
                work_size=8, is_finished=False, collaborators='4')
    job6 = Jobs(team_leader=3, job='data processing',
                work_size=18, is_finished=False, collaborators='3,5')
    job7 = Jobs(team_leader=1, job='module installation',
                work_size=25, is_finished=True, collaborators='1,2')

    db_sess.add(job1)
    db_sess.add(job2)
    db_sess.add(job3)
    db_sess.add(job4)
    db_sess.add(job5)
    db_sess.add(job6)
    db_sess.add(job7)
    db_sess.commit()


def init_data_deps():
    db_sess = db_session.create_session()
    dep1 = Department(title='геологическая разведка', chief=3, members=[4, 5], email='geology@mars.org')
    dep2 = Department(title='изучение явлений', chief=2, members=[3], email='phenomena@mars.org')
    dep3 = Department(title='инженерный отдел', chief=1, members=[1, 2, 3], email='engineering@mars.org')

    db_sess.add(dep1)
    db_sess.add(dep2)
    db_sess.add(dep3)
    db_sess.commit()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


@login_required
@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = JobsForm()
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    form.team_leader.choices = [(i.id, i.name) for i in users]

    if form.validate_on_submit():
        job = Jobs(
            job=form.job.data,
            work_size=form.work_size.data,
            team_leader=form.team_leader.data,
            is_finished=form.is_finished.data
        )
        if form.collaborators.data:
            job.collaborators = form.collaborators.data
        if form.start_date.data:
            job.start_date = form.start_date.data
        if form.end_date.data:
            job.end_date = form.end_date.data

        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjobs.html', title='Добавление работы', form=form)


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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


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
            email=form.email.data

        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.team_leader.data = jobs.team_leader
            form.is_finished.data = jobs.is_finished

        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.team_leader = form.team_leader.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')



def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(jobs_api.blueprint)
    # init_data_users()
    # init_data_jobs()
    # init_data_deps()

    # sess = db_session.create_session()
    # department = sess.query(Department).filter(Department.id == 1).first()
    #
    # if department and department.members:
    #
    #     total_hours_by_user = {}
    #
    #     for user_id in department.members:
    #         total_hours = 0
    #
    #         jobs = sess.query(Jobs).all()
    #
    #         for job in jobs:
    #             if job.team_leader == user_id:
    #                 total_hours += job.work_size
    #
    #             if job.collaborators:
    #                 collaborators = [int(x.strip()) for x in job.collaborators.split(',')]
    #                 if user_id in collaborators:
    #                     total_hours += job.work_size
    #
    #         total_hours_by_user[user_id] = total_hours
    #
    #     for user_id, total in total_hours_by_user.items():
    #         if total > 25:
    #             user = sess.get(User, user_id)
    #             if user:
    #                 print(f"{user.surname} {user.name}")

    app.run()


if __name__ == '__main__':
    main()
