from fastapi import FastAPI, HTTPException, Response
from classes import LoadProjectInput, ProjectDataInput
from utils import get_scene_mesh_names, get_current_blend_file_path, load_blend_file
from parser import get_mesh_data


app = FastAPI()


@app.get("/healthcheck")
async def root():
    return Response(status_code=200, content="OK")
    
@app.post("/project/load")
async def load_project(data: LoadProjectInput):
    file_path = data.file_path
    try:
        load_blend_file(file_path)
        meshes = get_scene_mesh_names()
        return {"meshes": meshes}
    except Exception as e:
       raise HTTPException(status_code=500, detail=f"Failed to load project: {e}")

@app.post("/project/data")
async def get_project_data(data: ProjectDataInput):
    file_path = data.file_path
    mesh_name = data.object_name

    current_file_path = get_current_blend_file_path()
    if current_file_path != file_path:
        load_blend_file(file_path)
    
    data = get_mesh_data(mesh_name)
    return data
