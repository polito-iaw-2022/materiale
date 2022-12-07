# import module
from flask import Flask, render_template, request, session, redirect, flash, url_for
from datetime import date, datetime
from flask_session import Session
import dao

# create the application
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# define the homepage


@app.route('/', methods=['GET', 'POST'])
def home():
    posts = dao.get_posts()

    if request.method == 'POST':
        session['usrname'] = request.form.get('usrname')
        return render_template('home.html', posts=posts)
    else:
        users = [d['nickname'] for d in posts]
        return render_template('home.html', posts=posts, users=users)


@app.route('/posts/<int:id>')
def single_post(id):
    post = dao.get_post(id)
    comments = dao.get_comments(post['id'])

    return render_template('post.html', post=post, comments=comments)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        if session['usrname']:

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
                post_image.save('static/' + post_image.filename)
                post['immagine_post'] = post_image.filename

            id_utente = dao.get_user_id(session['usrname'])
            post['id_utente'] = id_utente['id']

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

    id_utente = dao.get_user_id(session['usrname'])
    success = dao.add_comment(comment, id_utente['id'])

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
