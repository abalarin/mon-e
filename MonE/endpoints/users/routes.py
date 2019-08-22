from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt

from MonE import db
from MonE.models.users import User
from MonE.endpoints.users.forms import RegistrationForm
from MonE.endpoints.users.utils import date_now, user_exsists

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create user object to insert into SQL
        hashed_pass = sha256_crypt.encrypt(str(form.password.data))

        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_pass,
            join_date=date_now()
        )

        # Insert new user into SQL
        if user_exsists(new_user.username, new_user.email):
            flash('User already exsists!', 'danger')
            return render_template('users/register.html', form=form)
        else:

            try:
                db.session.add(new_user)
                db.session.commit()

                # Init session vars
                login_user(new_user)
            except Exception as e:
                flash('There was an issue, plz try again!', 'danger')
                print(e)
                # Clear any in-progress sqlalchemy transactions
                try:
                    db.session.rollback()
                except:
                    pass
                try:
                    db.session.remove()
                except:
                    pass

            return render_template('index.html', user=new_user)

    return render_template('users/register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')

    else:
        username = request.form.get('username')
        password_candidate = request.form.get('password')

        try:
            # Query for a user with the provided username
            result = User.query.filter_by(username=username).first()

        except Exception as e:
            flash('There was an issue, plz try again!', 'danger')
            print(e)
            # Clear any in-progress sqlalchemy transactions
            try:
                db.session.rollback()
            except:
                pass
            try:
                db.session.remove()
            except:
                pass

        # If a user exsists and passwords match - login
        if result is not None and sha256_crypt.verify(password_candidate, result.password):

            # Init session vars
            login_user(result)
            return redirect(url_for('users.dashboard'))

        else:
            flash('Incorrect Login!', 'danger')
            return render_template('users/login.html')


@users.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have logged out!', 'success')
    return redirect(url_for('main.index'))

@users.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('users/dashboard.html')
