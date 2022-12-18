from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_session import Session
import dao

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/iscriviti')
def signup():
    return render_template('signup.html')


@app.route('/iscriviti', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    password = request.form.get('password')

    user_in_db = dao.get_user_by_email(email)

    if user_in_db:
        flash('C\'è già un utente registrato con questa email', 'danger')
        return redirect(url_for('signup'))
    else:
        new_user = {
            "name": name,
            "surname": surname,
            "email": email,
            "password": generate_password_hash(password, method='sha256')
        }

        success = dao.add_user(new_user)

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')

    return redirect(url_for('signup'))


@app.route('/accedi')
def login():
    return render_template('login.html')


@app.route('/accedi', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = dao.get_user_by_email(email)

    if not user or not check_password_hash(user['password'], password):
        flash('Credenziali non valide, riprovare', 'danger')
        return redirect(url_for('login'))
    else:
        new = User(id=user['id'], name=user['nome'], surname=user['cognome'],
                   email=user['email'], password=user['password'])
        login_user(new, True)

        return redirect(url_for('profile'))


@app.route('/profilo')
@login_required
def profile():
    return render_template('profile.html')


@login_manager.user_loader
def load_user(user_id):

    db_user = dao.get_user_by_id(user_id)

    user = User(id=db_user['id'], name=db_user['nome'], surname=db_user['cognome'],
                email=db_user['email'], password=db_user['password'])

    return user


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
