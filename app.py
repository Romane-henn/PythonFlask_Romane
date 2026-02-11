# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Bienvenue sur ma page d'accueil ! <br><a href='http://127.0.0.1:5001/map'>Voir la carte</a>"

# @app.route('/map')
# def map():
#     return render_template("map.html")

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

import os
from flask import Flask, render_template, send_from_directory

# ... ton code existant ...

@app.route('/gallery')
def gallery():
    images = os.listdir(os.path.join('static', 'images'))
    return render_template("gallery.html", images=images)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
