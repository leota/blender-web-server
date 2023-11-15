import threading
import bpy
import sys
import os
sys.path.append('/Users/leonardo/.local/lib/python3.10/site-packages')

# Assuming server.py is in the same directory as your Blender script
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from server import app
import uvicorn

# Function to run the server in a separate thread
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Start the FastAPI server in a new thread
thread = threading.Thread(target=run_server)
thread.start()
