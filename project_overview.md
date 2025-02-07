Below is a detailed design report—our "project canvas"—that outlines the FaceTrace web application. This document explains the architecture, directory structure, modules, user flow, and other implementation considerations. It will serve as a blueprint for writing the code in subsequent phases.

---

# FaceTrace Project: Detailed Design Report

## 1. Overview

**FaceTrace** is a real-time face detection and recognition web application built using Python, Streamlit, OpenCV, and the `face_recognition` package. The primary goal is to monitor a live video feed from a camera, detect faces, count the number of persons present, and identify them by matching against a repository of pre-saved face data. Any face that is not recognized during the live session will be labeled dynamically as `Unknown_1`, `Unknown_2`, etc.

---

## 2. Objectives

- **Real-Time Monitoring:**\
  Capture video from the camera and process each frame to detect and recognize faces.

- **Face Recognition:**\
  Utilize the `face_recognition` package to generate face encodings and compare them with stored face data.

- **File System Data Storage:**\
  Save the data for known faces (face image and metadata) using a file system approach rather than a database. Each person's data will reside in a dedicated folder identified by their roll number.

- **User Interface:**\
  Build an intuitive Streamlit web interface that includes:

  - **Login Page:** Secure entry for the admin (credentials: username `admin` and password `admin`).
  - **Home Page:** Central hub with navigation options (Start Monitoring, Save New Face Data, View Saved Face Data, Logout).
  - **Monitoring Page:** Display the live video feed with real-time annotations (bounding boxes, face names, and count).
  - **Save New Face Data Page:** Form to add new face data by capturing an image and inputting details like name and roll number.
  - **View Saved Face Data Page:** Display the list of saved faces (read from the file system).

- **Dynamic Unknown Labeling:**\
  Faces that are not recognized during monitoring are dynamically labeled as `Unknown_1`, `Unknown_2`, etc., without saving these unknown images to disk.

---

## 3. Technology Stack

- **Python 3.10:**\
  Primary language for the application.

- **Streamlit:**\
  Framework for creating the web interface and handling page navigation.

- **OpenCV (**``**):**\
  For accessing the camera, processing video frames, and overlaying detection outputs.

- **face\_recognition:**\
  For detecting faces and generating numerical encodings for recognition.

- **Pillow (PIL):**\
  For image manipulation tasks if needed (e.g., resizing, format conversion).

- **NumPy:**\
  Essential for handling face encoding arrays.

- **File I/O (os, pathlib, etc.):**\
  For managing file system operations like creating directories, saving images, and writing metadata.

---

## 4. System Architecture & Modules

The project is divided into several logical modules, ensuring separation of concerns:

### A. **Presentation Layer (Streamlit UI)**

- **Authentication Module:**\
  Handles the admin login process and session state management.

- **Navigation and Page Routing:**\
  Provides multiple pages including login, home, monitoring, saving new face data, and viewing saved face data.

### B. **Face Processing Module**

- **Real-Time Face Detection & Recognition:**\
  Captures video frames using OpenCV, detects faces, extracts face encodings using `face_recognition`, and compares them with saved encodings.

- **Dynamic Labeling:**\
  Implements logic to assign labels to unknown faces (e.g., `Unknown_1`, `Unknown_2`, etc.) during live monitoring.

### C. **Data Management Module (File System Storage)**

- **Folder Structure for Saved Faces:**\
  Uses the file system to store known face data. Each known face is stored in a folder named after the roll number. This folder contains:

  - **Image File:** `{roll no.}.jpg`
  - **Metadata File:** `{roll no.}.txt` (contains details such as name, roll number, and possibly a serialized face encoding or summary info)

- **Utility Functions:**\
  Functions to create directories, write files, and read data from these folders.

---

## 5. Directory Structure

The project directory is organized as follows:

```
miniproject/
├── data/
│   └── saved/
│       ├── {roll_no_1}/
│       │   ├── {roll_no_1}.jpg
│       │   └── {roll_no_1}.txt
│       ├── {roll_no_2}/
│       │   ├── {roll_no_2}.jpg
│       │   └── {roll_no_2}.txt
│       └── ... (one folder per saved face)
├── utils/
│   ├── face_processing.py      # Functions related to face detection/recognition
│   ├── file_manager.py         # Functions for file system operations (saving, reading metadata, etc.)
│   └── authentication.py       # Functions for managing login and session state
└── app.py                      # Main application file; entry point for the Streamlit app
```

This structure keeps data, utility functions, and the main application logic well separated.

---

## 6. Detailed Module Descriptions

### A. **Authentication Module (**``**)**

- **Functionality:**
  - Validate user credentials.
  - Manage login session state within Streamlit.
  - Redirect to the home page on successful login.
- **Implementation Considerations:**
  - Hard-code the credentials (`admin`/`admin`) for now.
  - Use Streamlit’s session state to maintain logged-in status across pages.

### B. **Face Processing Module (**``**)**

- **Functionality:**
  - Capture video using OpenCV.
  - Detect faces in each frame using `face_recognition`.
  - Compute face encodings and compare them with encodings from saved files.
  - Draw bounding boxes and labels (including dynamic unknown labels) on the frames.
- **Implementation Considerations:**
  - Keep the processing loop efficient to support real-time operations.
  - Integrate OpenCV with Streamlit either by using Streamlit’s image display functions or a separate window.
  - Handle cases where no face is detected or multiple faces appear simultaneously.

### C. **File Management Module (**``**)**

- **Functionality:**
  - Create directories for new face data (using the roll number as the folder name).
  - Save images and metadata into the appropriate folder.
  - Read and list saved face data for the "View Saved Face Data" functionality.
- **Implementation Considerations:**
  - Use the `os` or `pathlib` libraries to manage file system paths.
  - Ensure proper error handling when reading/writing files.
  - Decide on a metadata format in the text file (e.g., JSON format or simple key-value pairs).

### D. **Streamlit Application (**``**)**

- **Functionality:**
  - Acts as the entry point for the application.
  - Set up routing and display different pages based on the user’s navigation.
  - Integrate with the utility modules to perform tasks such as starting the camera feed, saving new face data, and viewing saved data.
- **Implementation Considerations:**
  - Use Streamlit’s sidebar or navigation buttons to move between pages.
  - Ensure session state is properly maintained (especially login status).

---

## 7. User Flow

1. **Login Page:**

   - User is prompted to enter a username and password.
   - Credentials are validated (expected: `admin`/`admin`).
   - On success, the user is redirected to the Home Page.

2. **Home Page:**

   - Displays navigation options: **Start Monitoring**, **Save New Face Data**, **View Saved Face Data**, and **Logout**.
   - Logout option is available at the top-right corner.

3. **Start Monitoring:**

   - Activates the webcam feed.
   - Processes each frame to detect faces.
   - For each detected face:
     - Compares with saved data from `data/saved/`.
     - If a match is found, displays the corresponding name.
     - If not, assigns a dynamic label (e.g., `Unknown_1`).
   - Shows the total count of detected faces in the bottom-right corner.

4. **Save New Face Data:**

   - Provides a form for the admin to input:
     - Name
     - Roll Number
   - Captures an image (or selects one) of the face.
   - Creates a new folder under `data/saved/` named after the roll number.
   - Saves the face image (`{roll_no}.jpg`) and a text file (`{roll_no}.txt`) containing the metadata.

5. **View Saved Face Data:**

   - Lists all folders within `data/saved/` with summary details (name, roll number).
   - Optionally displays the face image for each entry.
   - Provides a simple way to verify the stored data.

6. **Logout:**

   - Ends the current session and redirects back to the login page.

---

## 8. Implementation Considerations

- **Performance:**\
  Ensure that the face detection and recognition processes are optimized for real-time performance. Consider processing frames at a reduced rate if needed.

- **Error Handling:**\
  Implement robust error handling especially for file I/O operations (e.g., handling missing folders, read/write errors).

- **User Experience:**\
  The Streamlit UI should be responsive and intuitive. Loading states, error messages, and confirmations should be provided where appropriate.

- **Extensibility:**\
  Although the feature to save unknown faces is removed for now, design the code modularly so that this feature can be added later with minimal changes.

- **Security:**\
  With hard-coded credentials, the application is only suitable for controlled environments. Future enhancements might include more robust authentication and role-based access.

---

## 9. Future Enhancements

- **Unknown Face Data Management:**\
  In future versions, incorporate a feature to store and manage unknown faces if required.

- **Improved User Management:**\
  Move beyond hard-coded credentials to a more secure authentication system.

- **Database Integration:**\
  If scaling becomes necessary, consider migrating from file system storage to a lightweight database (e.g., SQLite) for better data management and querying.

- **Enhanced Analytics:**\
  Provide additional insights such as attendance logs, frequency of appearances, etc.

---

## 10. Conclusion

This detailed report outlines the blueprint for the FaceTrace project. The application will be built using a modular approach with a clear separation between the user interface (via Streamlit), face processing logic (using OpenCV and face\_recognition), and data management (using the file system). The project directory is organized to keep code, data, and utilities neatly separated. With a well-defined user flow—from authentication to real-time monitoring and face data management—this design provides a solid foundation for proceeding to the coding phase.

Feel free to ask any questions or suggest modifications before we start implementing the code.
