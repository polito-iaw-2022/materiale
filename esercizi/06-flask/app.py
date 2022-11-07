# import module
from flask import Flask, render_template

# create the application
app = Flask(__name__)

# define the homepage
@app.route('/')
def index():
  return render_template('index.html')

# define the 'about' page
@app.route('/about.html')
def about():
  teachers = [
    {'id': 1234, 'name': 'Luigi De Russis'},
    {'id': 5678, 'name': 'Alberto Monge Roffarello'},
    {'id': 9012, 'name': 'Juan Pablo Sáenz Moreno'}
  ]
  return render_template('about.html', docenti=teachers)