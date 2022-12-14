# import module
from flask import Flask, render_template, request, session, redirect, flash, url_for
from datetime import date, datetime
from flask_session import Session
import dao

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

from PIL import Image

# create the application
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

PROFILE_IMG_HEIGHT = 130
POST_IMG_WIDTH = 300

# define the homepage


@app.route('/', methods=['GET', 'POST'])
def home():
    posts = dao.get_posts()

    return render_template('home.html', posts=posts)


@app.route('/posts/<int:id>')
def single_post(id):
    post = dao.get_post(id)
    comments = dao.get_comments(post['id'])

    return render_template('post.html', post=post, comments=comments)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        if current_user.is_authenticated:

            post = request.form.to_dict()

            if post['testo'] == '':
                app.logger.error('Il post non può essere vuoto!')
                flash(
                    'Post non creato correttamente: il post non può essere vuoto!', 'danger')
                return redirect(url_for('home'))

            if post['data_pubblicazione'] == '':
                app.logger.error('Devi selezionare una data')
                flash(
                    'Post non creato correttamente: devi selezionare una data!', 'danger')
                return redirect(url_for('home'))

            if datetime.strptime(post['data_pubblicazione'], '%Y-%m-%d').date() < date.today():
                app.logger.error('Data errata')
                flash(
                    'Post non creato correttamente: la data deve essere maggiore o uguale di quella corrente!', 'danger')
                return redirect(url_for('home'))

            post_image = request.files['immagine_post']
            if post_image:

                img = Image.open(post_image)

                width, height = img.size
                new_height = height/width * POST_IMG_WIDTH
                size = POST_IMG_WIDTH, new_height

                img.thumbnail(size, Image.ANTIALIAS)

                img.save('static/' + post_image.filename)
                post['immagine_post'] = post_image.filename

            id_utente = current_user.id
            post['id_utente'] = id_utente

            success = dao.add_post(post)

            if success:
                flash('Post creato correttamente', 'success')
            else:
                flash('Errore nella creazione del post: riprova!', 'danger')

    return redirect(url_for('home'))


@app.route('/comments/new', methods=['POST'])
def new_comment():
    comment = request.form.to_dict()
    if comment['testo'] == '':
        app.logger.error('Il commento non può essere vuoto!')
        flash(
            'Commento non creato correttamente: il commento non può essere vuoto!', 'danger')
        return redirect(url_for('single_post', id=comment['id_post']))

    id_utente = current_user.id
    success = dao.add_comment(comment, id_utente)

    if success:
        flash('Commento creato correttamente', 'success')
    else:
        flash('Errore nella creazione del commento: riprova!', 'danger')

    return redirect(url_for('single_post', id=comment['id_post']))


# define the 'about' page


@app.route('/about')
def about():
    p_developers = [
        {'id': 1234, 'name': 'Luigi De Russis', 'devimg': 'derussis.jpg',
            'quote': 'A well-known quote, contained in a blockquote element', 'quoteAuthor': 'First quote author'},
        {'id': 5678, 'name': 'Alberto Monge Roffarello', 'devimg': 'monge.jpg',
            'quote': 'A well-known quote, contained in a blockquote element', 'quoteAuthor': 'Second quote author'},
        {'id': 9012, 'name': 'Juan Pablo Sáenz', 'devimg': 'saenz.png',
            'quote': 'A well-known quote, contained in a blockquote element', 'quoteAuthor': 'Third quote author'}
    ]
    return render_template('about.html', developers=p_developers)


@login_manager.user_loader
def load_user(user_id):

    utente = dao.get_user_by_id(user_id)

    if utente is not None:
        user = User(id=utente['id'], nickname=utente['nickname'], password=utente['password'],
                    immagine_profilo=utente['immagine_profilo'])
    else:
        user = None

    return user


@app.route('/accedi')
def login():
    return render_template('login.html')


@app.route('/accedi', methods=['POST'])
def login_post():
    nickname = request.form.get('nickname')
    password = request.form.get('password')

    user = dao.get_user_by_nickname(nickname)

    if not user or not check_password_hash(user['password'], password):
        flash('Credenziali non valide, riprovare', 'danger')
        return redirect(url_for('login'))
    else:
        new = User(id=user['id'], nickname=user['nickname'], password=user['password'],
                   immagine_profilo=user['immagine_profilo'])
        login_user(new, True)

        return redirect(url_for('home'))


@app.route('/iscriviti')
def signup():
    return render_template('signup.html')


@app.route('/iscriviti', methods=['POST'])
def signup_post():
    nickname = request.form.get('nickname')
    password = request.form.get('password')

    user_in_db = dao.get_user_by_nickname(nickname)

    if user_in_db:
        flash('C\'è già un utente registrato con questo nickname', 'danger')
        return redirect(url_for('signup'))
    else:
        img_profilo = ''
        usr_image = request.files['immagine_profilo']
        if usr_image:
            img = Image.open(usr_image)

            width, height = img.size

            new_width = PROFILE_IMG_HEIGHT * width / height

            size = new_width, PROFILE_IMG_HEIGHT
            img.thumbnail(size, Image.ANTIALIAS)

            left = (new_width/2 - PROFILE_IMG_HEIGHT/2)
            top = 0
            right = (new_width/2 + PROFILE_IMG_HEIGHT/2)
            bottom = PROFILE_IMG_HEIGHT

            img = img.crop((left, top, right, bottom))

            ext = usr_image.filename.split('.')[1]

            img.save('static/' + nickname.lower() + '.' + ext)

            img_profilo = nickname.lower() + '.' + ext

        new_user = {
            "nickname": nickname,
            "password": generate_password_hash(password, method='sha256'),
            "immagine_profilo": img_profilo
        }

        success = dao.add_user(new_user)

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')

    return redirect(url_for('signup'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)