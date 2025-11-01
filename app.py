import cv2
import face_recognition
import pickle
import numpy as np
import base64
import io
from flask import Flask, request, jsonify, render_template
from PIL import Image

# --- Settings ---
ENCODING_FILE = "known_face.pkl"
TOLERANCE = 0.5

# --- 1. Load the Known Face Encoding (Do this once at startup) ---
print("Loading known face encoding...")
known_face_encoding = None
try:
    with open(ENCODING_FILE, 'rb') as f:
        known_face_encoding = pickle.load(f)
except FileNotFoundError:
    print(f"WARNING: Could not find encoding file '{ENCODING_FILE}'.")
    print("Please enroll a face using the web interface.")
except Exception as e:
    print(f"Error loading encoding file: {e}")

# --- 2. Initialize the Flask App ---
app = Flask(__name__)

# --- 3. Create a route to serve your index.html ---
@app.route('/')
def index():
    return render_template('index.html')

# --- 4. Create the API endpoint for CHECKING the face (Unlock) ---
@app.route('/check_face', methods=['POST'])
def check_face():
    global known_face_encoding
    if known_face_encoding is None:
        return jsonify({'status': 'Error', 'message': 'No face enrolled. Please enroll a face first.'})

    data = request.get_json()
    if 'image' not in data:
        return jsonify({'status': 'Error', 'message': 'No image data found'})

    try:
        header, encoded = data['image'].split(',', 1)
        image_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_data))
        frame_rgb = np.array(image)
    except Exception as e:
        return jsonify({'status': 'Error', 'message': f'Could not decode image: {e}'})
    
    face_locations = face_recognition.face_locations(frame_rgb)
    if not face_locations:
        return jsonify({'status': 'Unknown', 'message': 'No face found in image'})

    # Use the first face found
    try:
        face_encoding = face_recognition.face_encodings(frame_rgb, face_locations)[0]
    except IndexError:
         return jsonify({'status': 'Unknown', 'message': 'Could not encode face'})

    # Compare the new face to the known face
    matches = face_recognition.compare_faces([known_face_encoding], face_encoding, tolerance=TOLERANCE)

    if True in matches:
        return jsonify({'status': 'Access Granted', 'message': 'Access Granted!'})
    else:
        return jsonify({'status': 'Unknown', 'message': 'Access Denied: Unknown face'})

# --- 5. Create the API endpoint for ENROLLING a new face ---
@app.route('/enroll_face', methods=['POST'])
def enroll_face():
    global known_face_encoding
    
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'status': 'Error', 'message': 'No image data found'})

    # Decode the base64 image
    try:
        header, encoded = data['image'].split(',', 1)
        image_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_data))
        frame_rgb = np.array(image)
    except Exception as e:
        return jsonify({'status': 'Error', 'message': f'Could not decode image: {e}'})

    # Find faces (logic from enroll.py)
    face_locations = face_recognition.face_locations(frame_rgb)
    
    if len(face_locations) == 0:
        return jsonify({'status': 'Error', 'message': 'No face found. Please look at the camera and try again.'})
    elif len(face_locations) > 1:
        return jsonify({'status': 'Error', 'message': 'Multiple faces found. Only one person at a time, please.'})
    
    # --- Encode and Save Face ---
    try:
        face_encoding = face_recognition.face_encodings(frame_rgb, face_locations)[0]
        
        with open(ENCODING_FILE, 'wb') as f:
            pickle.dump(face_encoding, f)
        
        # IMPORTANT: Update the in-memory encoding for the /check_face route
        known_face_encoding = face_encoding
        
        print("New face enrolled and saved!")
        return jsonify({'status': 'Success', 'message': 'Face enrolled successfully!'})
    except Exception as e:
        print(f"Error during enrollment: {e}")
        return jsonify({'status': 'Error', 'message': f'Could not save encoding: {e}'})

# --- 6. Run the App ---
if __name__ == '__main__':
    print("Starting Flask server... Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True)