from flask import Flask, render_template
import os

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

@app.route('/gallery')
def gallery():
    images = os.listdir(os.path.join('static', 'images'))
    return render_template("gallery.html", images=images)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
