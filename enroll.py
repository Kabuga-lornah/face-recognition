import cv2
import face_recognition
import pickle
import os

# --- Settings ---
ENCODING_FILE = "known_face.pkl"
CAMERA_INDEX = 0  # 0 is usually the built-in webcam. Change if you have multiple.

# --- 1. Setup Camera ---
print("Starting camera... Look at the lens and press 's' to save your face.")
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

    # Display the live video feed
    # Flip the frame horizontally (like a mirror)
    frame_display = cv2.flip(frame, 1)
    cv2.imshow("Enrollment - Press 's' to save", frame_display)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    # --- 2. Save on 's' key press ---
    if key == ord('s'):
        print("Saving image...")
        
        # We use the original 'frame' (not the flipped one) for encoding
        # Convert the image from BGR (OpenCV) to RGB (face_recognition)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all faces in the image
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if len(face_locations) == 0:
            print("No face found. Please try again.")
        elif len(face_locations) > 1:
            print("Multiple faces found. Only one person at a time, please.")
        else:
            # --- 3. Encode and Save Face ---
            # Get the *first* (and only) face encoding
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            
            # Save this encoding to a file using pickle
            with open(ENCODING_FILE, 'wb') as f:
                pickle.dump(face_encoding, f)
            
            print(f"Success! Face encoding saved to {ENCODING_FILE}")
            break # Exit the loop after saving

    # --- 4. Quit on 'q' key press ---
    elif key == ord('q'):
        print("Enrollment cancelled.")
        break

# --- 5. Cleanup ---
cap.release()
cv2.destroyAllWindows()