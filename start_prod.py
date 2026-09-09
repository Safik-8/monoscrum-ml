import subprocess
import time
import os
import re
from pyngrok import ngrok

PORT = 8001
API_ENV_PATH = r"C:\Users\safik\Desktop\stackdot\monoscrum\mono-scrum-api\.env"

def main():
    print(f"Starting FastAPI server on port {PORT}...")
    
    # Start the server as a subprocess
    server_process = subprocess.Popen(
        ["venv\\Scripts\\python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", str(PORT)],
        shell=True
    )
    
    # Wait a bit for the server to start
    time.sleep(3)
    
    print(f"Starting ngrok tunnel on port {PORT}...")
    try:
        # Load NGROK_AUTHTOKEN from .env
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("NGROK_AUTHTOKEN="):
                        token = line.split("=", 1)[1].strip().strip('"').strip("'")
                        ngrok.set_auth_token(token)
                        break

        # Open a ngrok tunnel to the server
        public_url = ngrok.connect(PORT).public_url
        print(f"\n=================================================")
        print(f"🚀 Ngrok Tunnel Established: {public_url}")
        print(f"=================================================\n")
        
        # Update the mono-scrum-api .env file
        if os.path.exists(API_ENV_PATH):
            with open(API_ENV_PATH, "r", encoding="utf-8") as f:
                content = f.read()
                
            if "FACE_API_URL=" in content:
                # Replace existing FACE_API_URL
                content = re.sub(r'FACE_API_URL=.*', f'FACE_API_URL="{public_url}"', content)
            else:
                # Append if not exists
                content += f'\nFACE_API_URL="{public_url}"\n'
                
            with open(API_ENV_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"✅ Updated {API_ENV_PATH} with FACE_API_URL={public_url}")
        else:
            print(f"❌ Could not find {API_ENV_PATH}")
            
        print("\nPress Ctrl+C to stop the server and ngrok tunnel.")
        
        # Keep the script running
        server_process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        ngrok.kill()
        server_process.terminate()

if __name__ == "__main__":
    main()
