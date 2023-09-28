from flask import Flask, render_template, send_from_directory, request
import os

app = Flask(__name__)

NDT_PHOTOS_DIR = '/home/piracer/mycar/NDT_photos/'

@app.route('/')
def index():
    available_folders = [folder for folder in os.listdir(NDT_PHOTOS_DIR) if os.path.isdir(os.path.join(NDT_PHOTOS_DIR, folder))]
    return render_template('index.html', available_folders=available_folders)

@app.route('/view/<folder>')
def view_folder(folder):
    photo_dir = os.path.join(NDT_PHOTOS_DIR, folder)
    photos = [f for f in os.listdir(photo_dir) if f.endswith(('jpg', 'jpeg', 'png'))]
    return render_template('view_folder.html', photos=photos, folder=folder)

@app.route('/photos/<folder>/<filename>')
def get_photo(folder, filename):
    return send_from_directory(os.path.join(NDT_PHOTOS_DIR, folder), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
