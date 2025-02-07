from flask import Flask, request, jsonify, render_template
import os
from actions.google_drive_utils import download_images_from_drive
from actions.face_matching import match_faces
from actions.display_results import display_images
from actions.email_sender import send_email_with_images

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
MATCHED_FOLDER = "static/matched"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MATCHED_FOLDER, exist_ok=True)

drive_folder_id = "1Ck-RHRZVNSCqUUismv_XXg4_jAaTWRRk"  # Replace with actual folder ID

download_images_from_drive(drive_folder_id, MATCHED_FOLDER)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    matched_images = match_faces(file_path, MATCHED_FOLDER)
    
    user_email = request.form.get("email")  # Get email from frontend form
    if user_email:
        send_email_with_images(user_email, matched_images)
    
    return jsonify({'matched_images': matched_images})

if __name__ == '__main__':
    app.run(debug=True)
