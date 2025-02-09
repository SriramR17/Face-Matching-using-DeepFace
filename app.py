
from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from actions.google_drive_utils import download_images_from_drive
from actions.face_matching import match_faces
from actions.email_sender import send_email_with_images
import cv2
import numpy as np
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image
        google_drive_folder_id = "1Ck-RHRZVNSCqUUismv_XXg4_jAaTWRRk"  # Replace with your folder ID
        group_photos = download_images_from_drive(google_drive_folder_id)
        matched_images, unmatched_images = match_faces(filepath, group_photos)
        
        # Convert matched images to base64 for display
        matched_images_b64 = []
        for img in matched_images:
            _, buffer = cv2.imencode('.jpg', img)
            img_b64 = base64.b64encode(buffer).decode('utf-8')
            matched_images_b64.append(img_b64)
        
        # Send email if requested
        if request.form.get('send_email'):
            receiver_email = request.form.get('email')
            if receiver_email:
                send_email_with_images(receiver_email, matched_images)
        
        return jsonify({
            'success': True,
            'matched_images': matched_images_b64
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/capture', methods=['POST'])
def capture_image():
    # Handle webcam capture data
    image_data = request.json.get('image')
    if not image_data:
        return jsonify({'error': 'No image data received'}), 400
    
    # Convert base64 to image
    try:
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Save captured image
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'captured.jpg')
        cv2.imwrite(filepath, img)
        
        # Process the image (same as upload route)
        google_drive_folder_id = "1"
        group_photos = download_images_from_drive(google_drive_folder_id)
        matched_images, unmatched_images = match_faces(filepath, group_photos)
        
        # Convert matched images to base64
        matched_images_b64 = []
        for img in matched_images:
            _, buffer = cv2.imencode('.jpg', img)
            img_b64 = base64.b64encode(buffer).decode('utf-8')
            matched_images_b64.append(img_b64)
        
        return jsonify({
            'success': True,
            'matched_images': matched_images_b64
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'Email address is required'}), 400
        
    try:
        # Get the latest matched images
        if not os.path.exists('matched_images'):
            return jsonify({'error': 'No matched images found'}), 400
            
        matched_images = []
        for filename in os.listdir('matched_images'):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join('matched_images', filename)
                img = cv2.imread(img_path)
                if img is not None:
                    matched_images.append(img)
        
        if not matched_images:
            return jsonify({'error': 'No matched images found'}), 400
            
        # Send email
        send_email_with_images(email, matched_images)
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)