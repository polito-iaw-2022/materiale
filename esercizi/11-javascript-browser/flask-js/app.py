# import modules
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date
from flask_session import Session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import posts_dao
import users_dao
from models.User import User

# create the application
app = Flask(__name__)
app.secret_key = 'questa è una chiave segreta'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# login set-up
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Accedi per visualizzare questa pagina'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

# define the homepage
@app.route('/')
def index():
  posts = posts_dao.get_posts()
  return render_template('index.html', posts=posts)

# single post
@app.route('/posts/<int:id>')
def single_post(id):
  post = posts_dao.get_post(id)
  comments = posts_dao.get_comments(id)
  return render_template('single.html', post=post, comments=comments)

# about page
@app.route('/about')
def about():
  return render_template('about.html')

# new post -- must be logged-in
@app.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
  if request.method == 'POST':
    # app.logger.debug(request.form['title'])
    post = request.form.to_dict()
    # TODO: validare tutti i campi del form
    if post['title'] == '':
      # TODO: gestire errore
      app.logger.error('Il titolo non può essere vuoto!')
    # inserire default per la data
    if post['date'] == '':
      post['date'] = date.today()
    # salvo immagine dal form (se esiste)
    post_image = request.files['image']
    if post_image:
      post_image.save('static/' + post['title'].lower() + '.jpg')
    success = posts_dao.add_post(post, current_user.id)
    if success:
      flash('Post creato correttamente', 'success')
    else:
      flash('Errore nella creazione del post: riprova!', 'danger')
    return redirect(url_for('index'))
  else:
    return render_template('new-post.html')

# login page
@app.route('/login')
def login():
  return render_template('login.html')

# new login
@app.route('/login', methods=['POST'])
def new_login():
  email = request.form.get('email')
  password = request.form.get('password')

  user = users_dao.get_user_by_email(email)

  if not user or not check_password_hash(user['password'], password):
      flash('Credenziali non valide, riprova!', 'danger')
      return redirect(url_for('login'))
  else:
      new = User(id=user['id'], name=user['name'], surname=user['surname'],
                  email=user['email'], password=user['password'])
      login_user(new, True)

      return redirect(url_for('index'))

# to retrieve the logged-in user
@login_manager.user_loader
def load_user(user_id):
  db_user = users_dao.get_user_by_id(user_id)
  user = User(id=db_user['id'], name=db_user['name'], surname=db_user['surname'],
                email=db_user['email'], password=db_user['password'])

  return user

# logout
@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))
