from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue sur ma page d'accueil ! <br><a href='/map'>Voir la carte</a>"

@app.route('/map')
def map():
    return render_template("map.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
