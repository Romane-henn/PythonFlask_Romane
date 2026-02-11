# from flask import Flask, render_template
# import os

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route('/map')
# def map():
#     return render_template("map.html")

# @app.route('/about')
# def about():
#     return render_template("about.html")

# @app.route('/projects')
# def projects():
#     return render_template("projects.html")

# @app.route('/gallery')
# def gallery():
#     images = os.listdir(os.path.join('static', 'images'))
#     return render_template("gallery.html", images=images)

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)
import os
from flask import Flask, render_template, request, send_from_directory, url_for

app = Flask(__name__)

# Page d'accueil
@app.route('/')
def home():
    return render_template("index.html")

# Page À propos
@app.route('/about')
def about():
    return render_template("about.html")

# Page Carte
@app.route('/map')
def map_view():
    return render_template("map.html")

# Répertoire par défaut pour la galerie
REPERTOIRE_PAR_DEFAUT = "C:/Users"

# Page Galerie
@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        chemin_dossier = request.form.get('chemin', REPERTOIRE_PAR_DEFAUT)
    else:
        chemin_dossier = request.args.get('chemin', REPERTOIRE_PAR_DEFAUT)

    images = []
    erreur = None

    if os.path.exists(chemin_dossier):
        images = [f for f in os.listdir(chemin_dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    else:
        erreur = "Le répertoire est introuvable."

    image_choisie = request.args.get('image_selectionnee')

    return render_template('gallery.html',
                           images=images,
                           image_choisie=image_choisie,
                           chemin=chemin_dossier,
                           erreur=erreur)

# Route pour servir les images brutes
@app.route('/image_brute/<path:nom_image>')
def image_brute(nom_image):
    dossier = request.args.get('dossier')
    return send_from_directory(dossier, nom_image)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
