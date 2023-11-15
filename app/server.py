from fastapi import FastAPI, HTTPException
import bpy
from inputs import ImportProjectInput
from utils import get_scene_mesh_names, load_blend_file



# Create an instance of the FastAPI class
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI running in Blender!"}

@app.post("/import")
async def import_project(data: ImportProjectInput):
    file_path = data.file_path
    try:
        load_blend_file(file_path)
        return {"message": "Project successfully imported"}
    except Exception as e:
       raise HTTPException(status_code=500, detail=f"Failed to import project: {e}")



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
