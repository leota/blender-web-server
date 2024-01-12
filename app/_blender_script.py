import os
import platform
import sys
import bpy


SITE_PACKAGES_PATH = os.environ.get('SITE_PACKAGES_PATH')
sys.path.append(SITE_PACKAGES_PATH)

if platform.system() == "Linux":
    dist_packages_dirs = [
        "/usr/local/lib/python3.10/dist-packages",
        "/usr/lib/python3/dist-packages",
        "/usr/lib/python3.10/dist-packages",
    ]
    for dist_packages_dir in dist_packages_dirs:
        sys.path.append(dist_packages_dir)

# Assuming server.py is in the same directory as your _blender_script.py
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

from server import app
import uvicorn

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8080)

# Start the FastAPI server in a new thread (only if running in Blender graphics mode)
# import threading
# thread = threading.Thread(target=run_server)
# thread.start()

run_server()
