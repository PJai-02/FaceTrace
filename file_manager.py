# import os
# import cv2
# import uuid

# # Directory to store saved face images.
# DATA_DIR = "saved_faces"
# if not os.path.exists(DATA_DIR):
#     os.makedirs(DATA_DIR)

# # In-memory database for saved faces.
# # In production, consider using a persistent database.
# saved_faces_db = []

# def save_face_data(roll_no, name, img):
#     """
#     Saves the face image to disk and stores its info in a global list.
#     """
#     try:
#         filename = f"{name}_{roll_no}_{uuid.uuid4().hex}.jpg"
#         filepath = os.path.join(DATA_DIR, filename)
#         cv2.imwrite(filepath, img)
#         face_entry = {"roll_no": roll_no, "name": name, "image_path": filepath}
#         saved_faces_db.append(face_entry)
#         return True
#     except Exception as e:
#         print("Error saving face data:", e)
#         return False

# def get_all_saved_faces():
#     """
#     Returns the list of saved face entries.
#     """
#     return saved_faces_db

import os
import cv2
import uuid
import json

# Directory to store saved face images.
DATA_DIR = "saved_faces"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# JSON file to persist saved face metadata.
DB_FILE = "saved_faces_db.json"

def load_db():
    """Load the saved face metadata from the JSON file."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading database:", e)
            return []
    else:
        return []

def save_db(db):
    """Save the face metadata to the JSON file."""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=4)
    except Exception as e:
        print("Error saving database:", e)

def save_face_data(roll_no, name, img):
    """
    Saves the face image to disk and updates the persistent JSON database.
    Returns True if saving was successful, False otherwise.
    """
    try:
        filename = f"{name}_{roll_no}_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(DATA_DIR, filename)
        cv2.imwrite(filepath, img)
        face_entry = {"roll_no": roll_no, "name": name, "image_path": filepath}
        # Load the current database, update it, and save it back.
        db = load_db()
        db.append(face_entry)
        save_db(db)
        return True
    except Exception as e:
        print("Error saving face data:", e)
        return False

def get_all_saved_faces():
    """Returns the list of saved face entries from the persistent database."""
    return load_db()
