from fastapi import FastAPI, HTTPException
from classes import ImportProjectInput
from utils import get_scene_mesh_names, load_blend_file
from parser import get_mesh_data


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

@app.get("/mesh/{mesh_name}")
async def get_mesh(mesh_name: str):
    data = get_mesh_data(mesh_name)
    return data
