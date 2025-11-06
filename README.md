# Face Recognition System

## Project Overview

This project is a Python-based face recognition application that provides two main functionalities: enrolling new users by capturing and storing their face encodings, and a main application for real-time face detection and verification (unlock/access control). The system is built around a minimal web interface for a user-friendly experience.

## Features

  * **Face Enrollment:** A dedicated script to capture a user's image, process their facial features, and securely store the unique face encoding.
  * **Face Recognition/Verification:** A main application to process a real-time video feed, detect faces, and compare them against the database of known face encodings to verify identity.
  * **Web Interface:** Uses a simple HTML frontend to display the recognition process.
  * **Persistent Storage:** Face encodings of known users are stored in a persistent data file (`known_face.pkl`).

## Prerequisites

To run this project, you will need to have Python installed on your system. It is highly recommended to use a virtual environment.

  * Python 3.x
  * Required Python Packages (Likely including, but not limited to):
      * `face_recognition`
      * `opencv-python`
      * `Flask` (for the web application)

## Installation and Setup

1.  **Clone the Repository:**

    ```bash
    git clone [your-repository-url]
    cd face-recognition
    ```

2.  **Create and Activate a Virtual Environment:**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    *Note: The actual dependencies should be installed from a `requirements.txt` if one exists in the original project. Assuming common libraries:*

    ```bash
    pip install face-recognition Flask
    # You might also need dlib dependencies and opencv-python, depending on the environment.
    ```

## Usage

### 1\. Enrolling a New Face

Before recognition can occur, at least one face must be enrolled.

Run the `enroll.py` script, which will typically guide you through capturing a reference image and providing a name for the new user.

```bash
python enroll.py
```

This process updates the `known_face.pkl` data file with the new facial encoding.

### 2\. Running the Face Recognition Application

Start the main application to begin the face detection and recognition process.

```bash
python app.py
```

The application will likely start a web server. Open your web browser and navigate to the address shown in the console (usually `http://127.0.0.1:5000/`) to view the real-time recognition stream.

### 3\. Unlock Script (Alternative Use Case)

The `unlock.py` script can be used for a simple command-line interface or system integration where a single face check is required (e.g., to unlock a screen).

```bash
python unlock.py
```

## Project Structure

```
face-recognition/
├── app.py                 # Main application for face recognition (likely Flask web app).
├── enroll.py              # Script to register new users/faces.
├── unlock.py              # Script for a single-shot face verification/unlock check.
├── known_face.pkl         # Persistent storage file for known face encodings.
├── templates/
│   └── index.html         # Web interface template for the main application.
└── venv/                  # Virtual environment folder.
```
