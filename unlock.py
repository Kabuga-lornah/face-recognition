import cv2
import face_recognition
import pickle

# --- Settings ---
ENCODING_FILE = "known_face.pkl"
CAMERA_INDEX = 0  # 0 is usually the built-in webcam.
TOLERANCE = 0.5   # How strict the match is. Lower is stricter. 0.5 is a good default.

# --- 1. Load the Known Face Encoding ---
print("Loading known face encoding...")
try:
    with open(ENCODING_FILE, 'rb') as f:
        known_face_encoding = pickle.load(f)
except FileNotFoundError:
    print(f"Error: Could not find encoding file '{ENCODING_FILE}'.")
    print("Please run the 'enroll.py' script first to register your face.")
    exit()

# --- 2. Setup Camera ---
print("Starting camera... Looking for a match.")
cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print(f"Error: Could not open camera at index {CAMERA_INDEX}.")
    exit()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # --- 3. Find Faces and Compare ---
    # Find all face locations and encodings in the *current* frame
    # Convert from BGR (OpenCV) to RGB (face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    frame_display = cv2.flip(frame, 1) # Flip for mirror effect
    access_granted = False

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the new face to the known face
        matches = face_recognition.compare_faces([known_face_encoding], face_encoding, tolerance=TOLERANCE)
        
        name = "Unknown"
        color = (0, 0, 255) # Red for unknown

        if True in matches:
            name = "Access Granted"
            color = (0, 255, 0) # Green for match
            access_granted = True
        
        # --- 4. Draw Box and Label ---
        # Draw a box on the *flipped* frame
        cv2.rectangle(frame_display, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame_display, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame_display, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    # --- 5. Display Result ---
    cv2.imshow("Face Unlock System - Press 'q' to quit", frame_display)

    if access_granted:
        print("UNLOCKED!")
        # In a real app, you would add your unlock logic here.
        # For this demo, we'll just wait 3 seconds and quit.
        cv2.waitKey(3000) # Wait 3 seconds
        break # Exit the loop

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("System locked. Quitting.")
        break

# --- 6. Cleanup ---
cap.release()
cv2.destroyAllWindows()