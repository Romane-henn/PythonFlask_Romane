import os
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from sklearn.cluster import KMeans
from PIL import Image

app = Flask(__name__)

# Route Accueil
@app.route('/')
def home():
    # Style minimaliste pour l'accueil
    style = "<style>body{font-family:sans-serif;text-align:center;padding:50px;} a{text-decoration:none;color:white;background:#1877f2;padding:10px 20px;border-radius:5px;}</style>"
    return style + """
    <h1>Bienvenue sur mon application </h1>
    <a href="/photo">Accéder à la Galerie </a>
    """

# Route Galerie et Sélection
@app.route('/photo', methods=['GET', 'POST'])
def photo():
    images = []
    # On récupère les données du formulaire
    dossier_choisi = request.form.get('chemin_dossier', '')
    photo_selectionnee = request.form.get('menu_photos', '')

    # Normalisation du chemin pour Windows
    if dossier_choisi:
        dossier_choisi = os.path.normpath(dossier_choisi)
        if os.path.exists(dossier_choisi):
            try:
                # Liste les fichiers images
                images = [f for f in os.listdir(dossier_choisi) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            except Exception as e:
                print(f"Erreur d'accès : {e}")

    return render_template("photo.html", 
                           images=images, 
                           dossier=dossier_choisi, 
                           photo_finale=photo_selectionnee)

# Route Traitement  (K-Means)
@app.route('/process_kmeans', methods=['POST'])
def process_kmeans():
    dossier = os.path.normpath(request.form.get('dossier'))
    photo = request.form.get('photo')
    k = int(request.form.get('k', 5))

    path_input = os.path.join(dossier, photo)
    
    # --- Logique K-Means ---
    img = Image.open(path_input).convert('RGB')
    
    # Redimensionnement pour accélerer le calcul
    img_small = img.copy()
    img_small.thumbnail((400, 400)) 
    
    img_np = np.array(img_small)
    original_shape = img_np.shape
    pixels = img_np.reshape(-1, 3)

    #  : Groupement des couleurs
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = kmeans.fit_predict(pixels)
    colors = kmeans.cluster_centers_.astype('uint8')

    # Reconstruction de l'image segmentée
    new_pixels = colors[labels]
    new_img_np = new_pixels.reshape(original_shape)
    
    result_name = f"kmeans_{k}_{photo}"
    result_path = os.path.join(dossier, result_name)
    Image.fromarray(new_img_np).save(result_path)

    # Recharger la liste des images
    images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    return render_template("photo.html", 
                           images=images, 
                           dossier=dossier, 
                           photo_finale=result_name)

# Route Crucle : Permet d'afficher l'image sur Windows
@app.route('/image_externe/<path:filename>')
def image_externe(filename):
    directory = request.args.get('dir')
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)