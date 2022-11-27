# import module
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date
from flask_session import Session

# create the application
app = Flask(__name__)
#app.secret_key = 'questa è una chiave segreta' # per il flash pre-sessione server-side
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

posts = [
    {'id': 1, 'title': 'CSS', 'date': '2022-10-10', 'tag': 'css', 'content': 'CSS sta per Cascading Style Sheet e in questo post ne parleremo meglio.'},
    {'id': 2, 'title': 'HTML', 'date': '2022-10-04', 'tag': 'html', 'content': 'HTML sta per HyperText Markup Language e in questo post ne parleremo meglio.'}
  ]

# define the homepage
@app.route('/')
def index():
  return render_template('index.html', posts=posts)

@app.route('/posts/<int:id>')
def single_post(id):
  post = posts[id-1]
  return render_template('single.html', post=post)

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
    # aggiungo id
    post['id'] = posts[-1]['id'] + 1
    # aggiungo post ad array "posts"
    posts.append(post)
    flash('Post creato correttamente', 'success')
    return redirect(url_for('index'))
  else:
    return render_template('new-post.html')

@app.route('/amministratore')
def admin():
  session['admin'] = True
  return redirect(url_for('index'))