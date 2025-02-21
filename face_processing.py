import cv2
import face_recognition
import streamlit as st
import time
import numpy as np
from utils import file_manager

def get_available_cameras(max_indices=4):
    """
    Scans device indices 0 to max_indices-1 and returns a list of indices that can be opened.
    """
    available = []
    for i in range(max_indices):
        cap = cv2.VideoCapture(i)
        if cap is not None and cap.isOpened():
            available.append(i)
            cap.release()
    return available

def process_video_feed(camera_index):
    """
    Opens the camera at the provided index, detects faces in real time,
    compares them with saved face data, and overlays recognized names and face count.
    """
    # Load known faces from saved data
    saved_faces = file_manager.get_all_saved_faces()
    known_face_encodings = []
    known_face_names = []
    for face in saved_faces:
        image_path = face.get("image_path")
        image = cv2.imread(image_path)
        if image is None:
            continue
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(face.get("name", "Unknown"))
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        st.error(f"Unable to access camera at index {camera_index}.")
        return
    
    if "monitoring" not in st.session_state:
        st.session_state.monitoring = True

    # Provide a button to stop monitoring.
    st.button("Stop Monitoring", on_click=stop_monitoring)
    frame_placeholder = st.empty()

    while st.session_state.monitoring:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to grab frame.")
            break

        # Convert frame from BGR to RGB for face detection.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        # Compare each detected face with the known faces.
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
            face_names.append(name)

        # Draw rectangles and labels on the frame.
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1)

        # Overlay the face count.
        count_text = f"Faces: {len(face_locations)}"
        cv2.putText(frame, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(frame, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2, cv2.LINE_AA)

        frame_placeholder.image(frame, channels="BGR")
        time.sleep(0.03)

    cap.release()

def stop_monitoring():
    st.session_state.monitoring = False
