from fastapi import FastAPI
import subprocess

app = FastAPI()


@app.get("/render")
def render():
    blender_command = [
        "blender",
        "/app/projects/table.blend",
        "--background",
        "--python",
        "blender_script.py",
        "Procedural Table GN",
        "Bevel",
        "width",
        "1.0",
    ]
    subprocess.run(blender_command)
    return {"message": "Rendering started"}
