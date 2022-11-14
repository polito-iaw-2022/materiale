# import module
from flask import Flask, render_template

# create the application
app = Flask(__name__)

# define the homepage
@app.route('/')
def index():
  return render_template('index.html')