from fastapi import FastAPI
import bpy
from utils import get_scene_mesh_names

# Create an instance of the FastAPI class
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI running in Blender!"}

@app.get("/meshes")
async def get_meshes():
    meshes = get_scene_mesh_names()
    return {"meshes": meshes}

@app.get("/meshes/{mesh_name}")
async def get_mesh(mesh_name: str):
    # Get the current scene
    scene = bpy.context.scene

    # Get the cube object by name
    cube = scene.objects.get(mesh_name)

    # Check if the cube exists in the scene
    if cube:
        # Change the scale on the X-axis to modify the width
        # For example, setting the width to 2 times the original width
        cube.scale.x *= 2
    else:
        print("Cube object not found in the scene.")

    return {"mesh_name": mesh_name}
