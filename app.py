import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Dossier pour stocker les images
UPLOAD_FOLDER = os.path.join('static', 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fonction pour vérifier l'extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# Page Projets
@app.route('/projects')
def projects():
    return render_template("projects.html")

# Page Galerie
@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    erreur = None
    if request.method == 'POST':
        # Vérifie si des fichiers ont été envoyés
        if 'images' not in request.files:
            erreur = "Aucun fichier sélectionné."
        else:
            files = request.files.getlist('images')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    erreur = "Certains fichiers ne sont pas valides."

    # Lister toutes les images dans le dossier static/images
    images = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    image_choisie = request.args.get('image_selectionnee')

    return render_template('gallery.html',
                           images=images,
                           image_choisie=image_choisie,
                           erreur=erreur)

# Route pour afficher les images
@app.route('/image_brute/<filename>')
def image_brute(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

# import os
# from flask import Flask, render_template, request, send_from_directory, url_for

# app = Flask(__name__)

# # Page d'accueil
# @app.route('/')
# def home():
#     return render_template("index.html")

# # Page À propos
# @app.route('/about')
# def about():
#     return render_template("about.html")

# # Page Carte
# @app.route('/map')
# def map_view():
#     return render_template("map.html")

# # Répertoire par défaut pour la galerie
# REPERTOIRE_PAR_DEFAUT = "C:/Users"

# # Page Galerie
# @app.route('/gallery', methods=['GET', 'POST'])
# def gallery():
#     if request.method == 'POST':
#         chemin_dossier = request.form.get('chemin', REPERTOIRE_PAR_DEFAUT)
#     else:
#         chemin_dossier = request.args.get('chemin', REPERTOIRE_PAR_DEFAUT)

#     images = []
#     erreur = None

#     if os.path.exists(chemin_dossier):
#         images = [f for f in os.listdir(chemin_dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
#     else:
#         erreur = "Le répertoire est introuvable."

#     image_choisie = request.args.get('image_selectionnee')

#     return render_template('gallery.html',
#                            images=images,
#                            image_choisie=image_choisie,
#                            chemin=chemin_dossier,
#                            erreur=erreur)

# # Route pour servir les images brutes
# @app.route('/image_brute/<path:nom_image>')
# def image_brute(nom_image):
#     dossier = request.args.get('dossier')
#     return send_from_directory(dossier, nom_image)


# if __name__ == '__main__':
#     app.run(debug=True, port=5001)
