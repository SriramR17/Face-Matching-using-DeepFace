import cv2
import numpy as np
from deepface import DeepFace
from actions.face_detection import detect_faces

def match_faces(reference_image, group_photos, model_name="Facenet"):
    """ Matches faces using DeepFace and returns matched & unmatched images """
    ref_embedding = DeepFace.represent(reference_image, model_name=model_name)[0]["embedding"]
    
    matched_images = []
    unmatched_images = []

    for img_path in group_photos:
        img, faces = detect_faces(img_path)
        matched = False

        for (x, y, w, h) in faces:
            face_crop = img[y:y+h, x:x+w]
            try:
                group_embedding = DeepFace.represent(face_crop, model_name=model_name)[0]["embedding"]
                similarity = np.dot(ref_embedding, group_embedding) / (np.linalg.norm(ref_embedding) * np.linalg.norm(group_embedding))

                if similarity > 0.6:  # Matching threshold
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 4)  # Thick bounding box
                    matched_images.append(img)
                    matched = True
                    break  # Stop checking further faces if one matches
            except:
                continue

        if not matched:
            unmatched_images.append(img)

    return matched_images, unmatched_images
