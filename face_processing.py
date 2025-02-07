# import streamlit as st
# import cv2
# import face_recognition
# import numpy as np
# import time
# from utils.file_manager import get_all_saved_faces

# def load_saved_face_encodings():
#     """
#     Loads saved face images from the file system, computes their encodings,
#     and returns two lists: known_encodings and corresponding known_names.
#     Uses the more accurate 'cnn' model and num_jitters=1.
#     """
#     saved_faces = get_all_saved_faces()
#     known_encodings = []
#     known_names = []
    
#     for face in saved_faces:
#         image_path = face["image_path"]
#         # Load the image file (returns an RGB image)
#         image = face_recognition.load_image_file(image_path)
#         # Use the "cnn" model for more accurate face detection
#         face_locations = face_recognition.face_locations(image, model="cnn")
#         if face_locations:
#             # Compute the encoding with num_jitters=1 for better accuracy
#             encoding = face_recognition.face_encodings(image, face_locations, num_jitters=1)[0]
#             known_encodings.append(encoding)
#             known_names.append(face["name"])
#     return known_encodings, known_names

# def process_video_feed():
#     """
#     Opens the webcam, detects and recognizes faces in real time, and displays
#     the video feed using Streamlit. Unrecognized faces are always labeled as "Unknown".
#     Uses the 'cnn' model and increased num_jitters for improved accuracy.
#     """
#     known_encodings, known_names = load_saved_face_encodings()
    
#     video_capture = cv2.VideoCapture(0)
#     if not video_capture.isOpened():
#         st.error("Error: Could not open video capture.")
#         return

#     # Initialize a session state flag for stopping the monitoring loop.
#     if "stop_monitoring" not in st.session_state:
#         st.session_state["stop_monitoring"] = False

#     # Create a single Stop button with a unique key and an on_click callback.
#     def stop_callback():
#         st.session_state["stop_monitoring"] = True

#     st.button("Stop Monitoring", key="stop_monitoring_button", on_click=stop_callback)
#     frame_placeholder = st.empty()

#     while video_capture.isOpened() and not st.session_state["stop_monitoring"]:
#         ret, frame = video_capture.read()
#         if not ret:
#             st.error("Failed to grab frame")
#             break

#         # Resize for faster processing.
#         small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#         # Convert BGR to RGB and ensure contiguous memory layout.
#         rgb_small_frame = np.ascontiguousarray(cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB))

#         # Use "cnn" for face detection for higher accuracy.
#         face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
#         # Compute face encodings with num_jitters=1 for improved accuracy.
#         face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, num_jitters=1)

#         face_names = []
#         for face_encoding in face_encodings:
#             matches = face_recognition.compare_faces(known_encodings, face_encoding)
#             if True in matches:
#                 first_match_index = matches.index(True)
#                 name = known_names[first_match_index]
#             else:
#                 name = "Unknown"
#             face_names.append(name)

#         # Draw bounding boxes and labels on the original frame.
#         for (top, right, bottom, left), name in zip(face_locations, face_names):
#             # Scale back up since the frame was resized.
#             top *= 4
#             right *= 4
#             bottom *= 4
#             left *= 4
#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#             cv2.putText(frame, name, (left + 6, bottom - 6),
#                         cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

#         cv2.putText(frame, f"Count: {len(face_names)}", (frame.shape[1] - 150, frame.shape[0] - 20),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
#         frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
#         time.sleep(0.03)

#     video_capture.release()

# utils/face_processing.py
import streamlit as st
import cv2
import face_recognition
import numpy as np
import time
from utils.file_manager import get_all_saved_faces

def load_saved_face_encodings():
    """
    Loads saved face images from the file system, computes their encodings,
    and returns two lists: known_encodings and corresponding known_names.
    """
    saved_faces = get_all_saved_faces()
    known_encodings = []
    known_names = []
    
    for face in saved_faces:
        image_path = face["image_path"]
        image = face_recognition.load_image_file(image_path)
        # For higher accuracy you might consider using model="cnn" and num_jitters=1.
        face_locations = face_recognition.face_locations(image, model="cnn")
        if face_locations:
            encoding = face_recognition.face_encodings(image, face_locations, num_jitters=1)[0]
            known_encodings.append(encoding)
            known_names.append(face["name"])
    return known_encodings, known_names

def process_video_feed():
    """
    Opens the webcam, processes each frame to detect and recognize faces,
    and displays a live video feed using Streamlit. Unrecognized faces are
    always labeled as "Unknown". The stop flag is reset at the start so that
    monitoring can be initiated multiple times without a page reload.
    """
    # Reset the stop flag so that a new monitoring session always starts fresh.
    st.session_state["stop_monitoring"] = False

    known_encodings, known_names = load_saved_face_encodings()
    
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        st.error("Error: Could not open video capture.")
        return

    # Create the Stop button only once, using a unique key and an on_click callback.
    def stop_callback():
        st.session_state["stop_monitoring"] = True

    st.button("Stop Monitoring", key="stop_monitoring_button", on_click=stop_callback)
    
    # Placeholder for updating video frames.
    frame_placeholder = st.empty()

    while video_capture.isOpened() and not st.session_state["stop_monitoring"]:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Failed to grab frame")
            break

        # Resize frame for faster processing.
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert BGR (OpenCV) to RGB and ensure the array is contiguous.
        rgb_small_frame = np.ascontiguousarray(cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB))

        # Use "cnn" for face detection for improved accuracy.
        face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")
        # Compute face encodings with num_jitters=1 for higher accuracy.
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, num_jitters=1)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
            else:
                name = "Unknown"
            face_names.append(name)

        # Draw bounding boxes and labels on the original frame.
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        cv2.putText(frame, f"Count: {len(face_names)}", (frame.shape[1] - 150, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
        time.sleep(0.03)

    video_capture.release()
