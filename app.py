import streamlit as st
import cv2
import numpy as np
from utils import authentication, face_processing, file_manager
import face_recognition

def login_page():
    st.title("FaceTrace Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authentication.login(username, password):
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")
            # Session state update will trigger a re-run naturally.
        else:
            st.error("Invalid credentials. Please try again.")

def home_page():
    st.title("FaceTrace Home")
    st.write("Welcome to FaceTrace!")
    st.write("Use the sidebar to navigate through the application.")

def start_monitoring_page():
    st.title("Start Monitoring")
    st.write("Select a camera and click 'Start Monitoring' to begin face monitoring.")

    # Enumerate available cameras
    available_cameras = face_processing.get_available_cameras()
    if not available_cameras:
        st.error("No cameras found!")
        return

    camera_index = st.selectbox("Select Camera", available_cameras, index=0)
    if st.button("Start Monitoring"):
        face_processing.process_video_feed(camera_index)

def save_new_face_page():
    st.title("Save New Face Data")
    st.write("Add a new face data entry by either capturing from the camera or uploading an image from your computer.")
    
    with st.form("save_face_form"):
        name = st.text_input("Name")
        roll_no = st.text_input("Roll Number")
        source_option = st.radio("Select Image Source", ("Capture from Camera", "Upload from Computer"), key="image_source")
        if source_option == "Capture from Camera":
            image_data = st.camera_input("Capture Face Image", key="camera_input")
        else:
            image_data = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png"], key="file_upload")
        
        submitted = st.form_submit_button("Save Face Data")
        if submitted:
            if name and roll_no and image_data is not None:
                file_bytes = np.asarray(bytearray(image_data.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                # Optionally, detect and crop the face from the captured image.
                face_locations = face_recognition.face_locations(img)
                if face_locations:
                    top, right, bottom, left = face_locations[0]
                    face_img = img[top:bottom, left:right]
                else:
                    face_img = img
                success = file_manager.save_face_data(roll_no, name, face_img)
                if success:
                    st.success("Face data saved successfully!")
                else:
                    st.error("Failed to save face data. Please try again.")
            else:
                st.error("Please fill in all the details and provide an image.")

def view_saved_faces_page():
    st.title("View Saved Face Data")
    saved_faces = file_manager.get_all_saved_faces()
    if not saved_faces:
        st.write("No saved face data found.")
    else:
        for face in saved_faces:
            st.subheader(f"Roll No: {face['roll_no']} - {face['name']}")
            st.image(face["image_path"], width=200)

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", 
                                ("Home", "Start Monitoring", "Save New Face Data", "View Saved Face Data", "Logout"))
        if page == "Home":
            home_page()
        elif page == "Start Monitoring":
            start_monitoring_page()
        elif page == "Save New Face Data":
            save_new_face_page()
        elif page == "View Saved Face Data":
            view_saved_faces_page()
        elif page == "Logout":
            authentication.logout()
            st.session_state["logged_in"] = False
            st.success("Logged out successfully!")

if __name__ == "__main__":
    main()
