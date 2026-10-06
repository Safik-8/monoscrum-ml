import base64
import numpy as np
import cv2
import face_recognition

class FaceService:
    def extract_embedding(self, image_base64: str) -> list[float]:
        # Decode base64
        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]
        
        img_data = base64.b64decode(image_base64)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Invalid image data")

        # Convert to RGB (face_recognition expects RGB)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Optimization: Resize the image to speed up face detection by 10x
        # A max dimension of 400px drops inference time from ~3s down to ~200ms
        max_dim = 400
        h, w = rgb_img.shape[:2]
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            rgb_img = cv2.resize(rgb_img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

        # Detect face locations
        # model="hog" is default and fastest on CPU
        face_locations = face_recognition.face_locations(rgb_img, model="hog")
        if not face_locations:
            raise ValueError("No face detected in the image")
        if len(face_locations) > 1:
            raise ValueError("Multiple faces detected. Please ensure only one face is in the frame.")

        # Extract embeddings (128-dimensional vector)
        face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
        if not face_encodings:
            raise ValueError("Could not extract facial features")

        # Return as list of floats
        return face_encodings[0].tolist()

face_service = FaceService()
