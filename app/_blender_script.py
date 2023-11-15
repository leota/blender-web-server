import sys
import platform
import bpy
import os

if platform.system() == 'Darwin':
    # macOS
    sys.path.append('/Users/leonardo/.local/lib/python3.10/site-packages')
else:
    # Linux
    sys.path.append('/usr/local/lib/python3.10/dist-packages')

# Assuming server.py is in the same directory as your Blender script
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from server import app
import uvicorn

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Start the FastAPI server in a new thread (only if running in Blender graphics mode)
# import threading
# thread = threading.Thread(target=run_server)
# thread.start()

run_server()
