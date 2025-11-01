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
try:
    with open(ENCODING_FILE, 'rb') as f:
        known_face_encoding = pickle.load(f)
except FileNotFoundError:
    print(f"FATAL ERROR: Could not find encoding file '{ENCODING_FILE}'.")
    print("Please run 'enroll.py' first.")
    exit()

# --- 2. Initialize the Flask App ---
app = Flask(__name__)

# --- 3. Create a route to serve your index.html ---
@app.route('/')
def index():
    # This will send the index.html file (which we will create)
    return render_template('index.html')

# --- 4. Create the API endpoint for checking the face ---
@app.route('/check_face', methods=['POST'])
def check_face():
    # Get the image data from the browser's request
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'status': 'Error', 'message': 'No image data found'})

    # Decode the base64 image
    # The data URL is "data:image/jpeg;base64,..."
    # We need to split off the header ("data:image/jpeg;base64,")
    try:
        header, encoded = data['image'].split(',', 1)
        image_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_data))
        # Convert PIL image to OpenCV format (RGB)
        frame_rgb = np.array(image)
    except Exception as e:
        return jsonify({'status': 'Error', 'message': f'Could not decode image: {e}'})
    
    # --- 5. Run the *exact same* face recognition logic ---
    face_locations = face_recognition.face_locations(frame_rgb)
    if not face_locations:
        return jsonify({'status': 'Unknown', 'message': 'No face found'})

    # Use the first face found
    face_encoding = face_recognition.face_encodings(frame_rgb, face_locations)[0]

    # Compare the new face to the known face
    matches = face_recognition.compare_faces([known_face_encoding], face_encoding, tolerance=TOLERANCE)

    if True in matches:
        return jsonify({'status': 'Access Granted'})
    else:
        return jsonify({'status': 'Unknown'})

# --- 6. Run the App ---
if __name__ == '__main__':
    print("Starting Flask server... Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True)