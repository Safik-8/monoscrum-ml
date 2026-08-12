import base64
import requests
import sys
import json

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded_string}"

def test_enroll(image_path, user_id):
    url = "http://127.0.0.1:8001/api/v1/scan/enroll"
    payload = {
        "image_base64": image_to_base64(image_path),
        "user_id": user_id
    }
    response = requests.post(url, json=payload)
    print("--- ENROLL RESPONSE ---")
    print(json.dumps(response.json(), indent=2))

def test_verify(image_path, device_id="test_device"):
    url = "http://127.0.0.1:8001/api/v1/scan/verify"
    payload = {
        "image_base64": image_to_base64(image_path),
        "device_id": device_id
    }
    response = requests.post(url, json=payload)
    print("\n--- VERIFY RESPONSE ---")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test.py <path_to_image.jpg> <user_id>")
        sys.exit(1)
        
    img_path = sys.argv[1]
    uid = sys.argv[2]
    
    # 1. Enroll the face
    print(f"Enrolling face from {img_path} for user {uid}...")
    test_enroll(img_path, uid)
    
    # 2. Verify the face
    print(f"\nVerifying face from {img_path}...")
    test_verify(img_path)
