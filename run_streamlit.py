import os
import subprocess

if __name__ == "__main__":
    # Start the Flask API server in a separate process
    api_process = subprocess.Popen(["python", "main.py"])
    
    # Start the Streamlit application
    os.system("streamlit run ui/streamlit_app.py")
    
    # Ensure the API server is terminated when this script exits
    api_process.terminate()