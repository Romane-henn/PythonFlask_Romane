# import os
# import numpy as np
# from flask import Flask, render_template, request, send_from_directory
# from sklearn.cluster import AgglomerativeClustering
# from scipy.cluster.hierarchy import dendrogram, linkage
# from PIL import Image
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import io
# import base64

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template("index.html")

# @app.route('/about')
# def about():
#     return render_template("about.html")

# @app.route('/map')
# def map():
#     return render_template("map.html")
# @app.route('/projects')
# def projects(): 
#     return render_template("projects.html")
# @app.route('/kmeans', methods=['GET', 'POST'])
# def kmeans():
#     images = []
#     dossier = request.form.get('dossier', '')
    
#     # Si on arrive sur la page via un formulaire (POST)
#     if request.method == 'POST' and dossier:
#         dossier = os.path.normpath(dossier)
#         if os.path.exists(dossier):
#             images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
#     # On retourne le template (vérifie bien que le fichier s'appelle kmeans.html)
#     return render_template("kmeans.html", images=images, dossier=dossier)

# @app.route('/hierarchie', methods=['GET', 'POST'])
# def hierarchie():
#     images = []
#     dossier = request.form.get('dossier', '')
#     photo = request.form.get('photo', '')
#     k_val = request.form.get('k', '3') # Nombre de clusters K
    
#     plot_url = None
#     result_image = None

#     if dossier:
#         dossier = os.path.normpath(dossier)
#         if os.path.exists(dossier):
#             images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

#     if photo and dossier:
#         path_input = os.path.join(dossier, photo)
#         img = Image.open(path_input).convert('RGB')
        
#         # --- 1. DENDROGRAMME (Sur miniature 45x45 pour la rapidité) ---
#         img_mini = img.copy()
#         img_mini.thumbnail((45, 45)) 
#         pixels_mini = np.array(img_mini).reshape(-1, 3)
#         Z = linkage(pixels_mini, method='complete')
        
#         plt.figure(figsize=(10, 5))
#         dendrogram(Z, truncate_mode='lastp', p=20)
#         plt.title(f"Analyse de l'arbre - {photo}")
        
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         buf.seek(0)
#         plot_url = base64.b64encode(buf.getvalue()).decode()
#         plt.close()

#         # --- 2. SEGMENTATION (Découpe en K clusters) ---
#         if k_val.isdigit():
#             K = int(k_val)
#             # Taille de l'image de sortie (on réduit à 150px pour que le HC ne fige pas l'ordi)
#             img_seg = img.copy()
#             img_seg.thumbnail((150, 150)) 
#             pix_array = np.array(img_seg)
#             h, w, c = pix_array.shape
#             pix_flat = pix_array.reshape(-1, 3)
            
#             # Application du modèle Agglomerative (comme ta prof)
#             model = AgglomerativeClustering(n_clusters=K, metric='euclidean', linkage='complete')
#             labels = model.fit_predict(pix_flat)
            
#             # Création de l'image segmentée : on remplace chaque pixel par la couleur moyenne du cluster
#             new_pixels = np.zeros_like(pix_flat)
#             for i in range(K):
#                 indices = (labels == i)
#                 if np.any(indices):
#                     # Calcul de la couleur moyenne du cluster i
#                     couleur_moyenne = np.mean(pix_flat[indices], axis=0)
#                     new_pixels[indices] = couleur_moyenne
            
#             # Reconstruction et sauvegarde
#             img_final = Image.fromarray(new_pixels.reshape(h, w, c).astype('uint8'))
#             result_name = f"segmentation_K{K}_{photo}"
#             img_final.save(os.path.join(dossier, result_name))
#             result_image = result_name

#     return render_template("hierarchie.html", 
#                            images=images, 
#                            dossier=dossier, 
#                            photo_origine=photo, 
#                            plot_url=plot_url, 
#                            result_image=result_image, 
#                            k=k_val)

# @app.route('/image_externe/<path:filename>')
# def image_externe(filename):
#     directory = request.args.get('dir')
#     return send_from_directory(directory, filename)

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

import os
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

# --- MODULE K-MEANS ---
@app.route('/kmeans', methods=['GET', 'POST'])
def kmeans():
    images = []
    dossier = request.form.get('dossier', '')
    if dossier:
        dossier = os.path.normpath(dossier)
        if os.path.exists(dossier):
            images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return render_template("kmeans.html", images=images, dossier=dossier)

@app.route('/kmeans_process', methods=['POST'])
def kmeans_process():
    dossier = os.path.normpath(request.form.get('dossier'))
    photo = request.form.get('photo')
    k = int(request.form.get('k', 5))
    
    path_input = os.path.join(dossier, photo)
    img = Image.open(path_input).convert('RGB')
    img.thumbnail((400, 400))
    pix = np.array(img)
    pix_flat = pix.reshape(-1, 3)

    # Algorithme K-Means
    kmeans = KMeans(n_clusters=k, n_init=10)
    labels = kmeans.fit_predict(pix_flat)
    centers = kmeans.cluster_centers_.astype('uint8')
    new_pix = centers[labels].reshape(pix.shape)

    result_name = f"result_kmeans_k{k}_{photo}"
    Image.fromarray(new_pix).save(os.path.join(dossier, result_name))

    # On recharge la liste des images pour l'affichage
    images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return render_template("kmeans.html", images=images, dossier=dossier, result_image=result_name, photo_origine=photo)

# --- MODULE HIÉRARCHIE ---
@app.route('/hierarchie', methods=['GET', 'POST'])
def hierarchie():
    images = []
    dossier = request.form.get('dossier', '')
    photo = request.form.get('photo', '')
    k_val = request.form.get('k', '3')
    plot_url = None
    result_image = None

    if dossier:
        dossier = os.path.normpath(dossier)
        if os.path.exists(dossier):
            images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if photo and dossier:
        path_input = os.path.join(dossier, photo)
        img = Image.open(path_input).convert('RGB')
        
        # Dendrogramme
        img_mini = img.copy()
        img_mini.thumbnail((40, 40))
        pix_mini = np.array(img_mini).reshape(-1, 3)
        Z = linkage(pix_mini, method='complete')
        
        plt.figure(figsize=(10, 5))
        dendrogram(Z, truncate_mode='lastp', p=20)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode()
        plt.close()

        # Segmentation
        k = int(k_val)
        img_seg = img.copy()
        img_seg.thumbnail((150, 150))
        pix_seg = np.array(img_seg)
        h, w, c = pix_seg.shape
        pix_flat = pix_seg.reshape(-1, 3)
        
        model = AgglomerativeClustering(n_clusters=k, linkage='complete')
        labels = model.fit_predict(pix_flat)
        
        new_pix = np.zeros_like(pix_flat)
        for i in range(k):
            mask = (labels == i)
            if np.any(mask):
                new_pix[mask] = np.mean(pix_flat[mask], axis=0)
        
        result_name = f"result_hc_k{k}_{photo}"
        Image.fromarray(new_pix.reshape(h, w, c).astype('uint8')).save(os.path.join(dossier, result_name))
        result_image = result_name

    return render_template("hierarchie.html", images=images, dossier=dossier, plot_url=plot_url, result_image=result_image, k=k_val, photo_origine=photo)

@app.route('/image_externe/<path:filename>')
def image_externe(filename):
    directory = request.args.get('dir')
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)