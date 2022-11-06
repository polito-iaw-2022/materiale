# import module
from flask import Flask

# create the application
app = Flask(__name__)

# define the homepage
@app.route('/')
def index():
  return """<html><head><title>IAW - Home</title></head>
    <body><h1>Blog di Introduzione alle Applicazioni Web</h1>
    <p>Benvenuto sul blog del corso.</p>
    <p><img src="static/logo.png"></p>
    <p>&copy; <a href="about.html">Introduzione alle Applicazioni Web</a></p>
    </body></html>
    """


# define the 'about' page
@app.route('/about.html')
def about():
  return """<html><head><title>IAW - Sul corso</title></head>
    <body><h1>Introduzione alle Applicazioni Web - Informazioni</h1>
    <p>Il corso &egrave; offerto al terzo anno delle lauree in Ingegneria al Politecnico di Torino.</p>
    <p>Questo esempio &egrave; stato creato nell'anno accademico 2022/2023.</p>
    <p><a href="/">Torna al blog</a></p>
    </body></html>
    """