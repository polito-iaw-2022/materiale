# import modules
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date
from flask_session import Session
import posts_dao

# create the application
app = Flask(__name__)
#app.secret_key = 'questa è una chiave segreta' # per il flash pre-sessione server-side
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# define the homepage
@app.route('/')
def index():
  posts = posts_dao.get_posts()
  return render_template('index.html', posts=posts)

@app.route('/posts/<int:id>')
def single_post(id):
  post = posts_dao.get_post(id)
  comments = posts_dao.get_comments(id)
  return render_template('single.html', post=post, comments=comments)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/posts/new', methods=['GET', 'POST'])
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
    success = posts_dao.add_post(post)
    if success:
      flash('Post creato correttamente', 'success')
    else:
      flash('Errore nella creazione del post: riprova!', 'danger')
    return redirect(url_for('index'))
  else:
    return render_template('new-post.html')

@app.route('/amministratore')
def admin():
  session['admin'] = True
  return redirect(url_for('index'))