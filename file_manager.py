# # utils/file_manager.py
# import os
# import json
# from pathlib import Path
# import cv2

# # Base directory where saved face data will be stored
# DATA_DIR = Path("data/saved")

# def save_face_data(roll_no: str, name: str, image) -> bool:
#     """
#     Saves the captured face image and metadata to a new folder named after the roll number.
    
#     Parameters:
#         roll_no: Unique roll number (string) that will be used as the folder name.
#         name: Name of the person.
#         image: The image (as an OpenCV BGR image) to be saved.
    
#     Returns:
#         True if data is saved successfully, else False.
#     """
#     try:
#         # Create folder for the given roll number if it doesn't exist
#         folder_path = DATA_DIR / roll_no
#         folder_path.mkdir(parents=True, exist_ok=True)
        
#         # Save image as {roll_no}.jpg
#         image_path = folder_path / f"{roll_no}.jpg"
#         cv2.imwrite(str(image_path), image)
        
#         # Save metadata as {roll_no}.txt in JSON format
#         metadata = {"roll_no": roll_no, "name": name}
#         metadata_path = folder_path / f"{roll_no}.txt"
#         with open(metadata_path, "w") as f:
#             json.dump(metadata, f)
            
#         return True
#     except Exception as e:
#         print(f"Error saving face data: {e}")
#         return False

# def get_all_saved_faces() -> list:
#     """
#     Retrieves a list of dictionaries containing saved face data.
    
#     Each dictionary contains:
#         - roll_no: The folder name (roll number)
#         - name: Person's name from metadata
#         - image_path: Path to the saved face image
#     """
#     saved_faces = []
#     if DATA_DIR.exists():
#         for folder in DATA_DIR.iterdir():
#             if folder.is_dir():
#                 metadata_path = folder / f"{folder.name}.txt"
#                 image_path = folder / f"{folder.name}.jpg"
#                 if metadata_path.exists() and image_path.exists():
#                     try:
#                         with open(metadata_path, "r") as f:
#                             metadata = json.load(f)
#                         saved_faces.append({
#                             "roll_no": folder.name,
#                             "name": metadata.get("name", ""),
#                             "image_path": str(image_path)
#                         })
#                     except Exception as e:
#                         print(f"Error reading metadata for {folder.name}: {e}")
#     return saved_faces

# utils/file_manager.py
import os
import json
from pathlib import Path
import cv2
import numpy as np
import face_recognition

# Base directory for saved face data
DATA_DIR = Path("data/saved")

def save_face_data(roll_no: str, name: str, image) -> bool:
    """
    Saves the captured face image, metadata, and computed face encoding 
    (using NumPy's .npy format) to a folder named after the roll number.
    
    Parameters:
        roll_no: Unique roll number (used as the folder name).
        name: Name of the person.
        image: The image (BGR format as read by OpenCV) to be saved.
    
    Returns:
        True if saving is successful; False otherwise.
    """
    try:
        # Create folder for this face data if it doesn't exist.
        folder_path = DATA_DIR / roll_no
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Save the face image as {roll_no}.jpg.
        image_path = folder_path / f"{roll_no}.jpg"
        cv2.imwrite(str(image_path), image)
        
        # Save metadata as JSON in {roll_no}.txt.
        metadata = {"roll_no": roll_no, "name": name}
        metadata_path = folder_path / f"{roll_no}.txt"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)
        
        # Convert image from BGR to RGB for face_recognition processing.
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(image_rgb)
        if face_locations:
            # Compute the encoding (using num_jitters=0 for speed).
            encoding = face_recognition.face_encodings(image_rgb, face_locations, num_jitters=0)[0]
            # Save the encoding as a .npy file.
            encoding_path = folder_path / f"{roll_no}_encoding.npy"
            np.save(str(encoding_path), encoding)
        else:
            print("No face detected in the saved image.")
            
        return True
    except Exception as e:
        print(f"Error saving face data: {e}")
        return False

def get_all_saved_faces() -> list:
    """
    Retrieves saved face data as a list of dictionaries.
    
    Each dictionary contains:
        - roll_no: The folder name (roll number)
        - name: Person's name (from metadata)
        - image_path: Path to the saved face image
    """
    saved_faces = []
    if DATA_DIR.exists():
        for folder in DATA_DIR.iterdir():
            if folder.is_dir():
                metadata_path = folder / f"{folder.name}.txt"
                image_path = folder / f"{folder.name}.jpg"
                if metadata_path.exists() and image_path.exists():
                    try:
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)
                        saved_faces.append({
                            "roll_no": folder.name,
                            "name": metadata.get("name", ""),
                            "image_path": str(image_path)
                        })
                    except Exception as e:
                        print(f"Error reading metadata for {folder.name}: {e}")
    return saved_faces
