from flask import Flask, render_template, request, redirect, url_for, flash
import dao

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'


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

    return redirect(url_for('signup'))


@app.route('/accedi')
def login():
    return render_template('login.html')


@app.route('/accedi', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    return redirect(url_for('home'))


@app.route('/profilo')
def profile():
    return render_template('profile.html')


@app.route("/logout")
def logout():
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
