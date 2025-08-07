from pyngrok import ngrok
import subprocess
import time

# Kill previous tunnels
ngrok.kill()
!kill $(pgrep ngrok)

# Set your ngrok authtoken
!ngrok authtoken "INPUT UR NGROK AUTH TOKEN"

# Start ngrok tunnel
public_url = ngrok.connect(8501).public_url
print(f"🔗 Public URL: {public_url}")

# Run Streamlit app in background
proc = subprocess.Popen(["streamlit", "run", "app.py"])

print("Streamlit app running...")
