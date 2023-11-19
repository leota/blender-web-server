from config import Settings
from fastapi import FastAPI, HTTPException, Response
from classes import LoadProjectInput, ProjectDataInput, RenderProjectInput, OutputFormat
from utils import get_scene_mesh_names, get_current_blend_file_path, load_blend_file, get_local_file_path
from parser import get_mesh_data
from render import render_object

env = Settings()
app = FastAPI()


@app.get("/healthcheck")
async def root():
    return Response(status_code=200, content="OK")
    
@app.post("/project/load")
async def load_project(data: LoadProjectInput):
    file_path = get_local_file_path(data.file_path)
    try:
        load_blend_file(file_path)
        meshes = get_scene_mesh_names()
        return {"meshes": meshes}
    except Exception as e:
       raise HTTPException(status_code=500, detail=f"Failed to load project: {e}")

@app.post("/project/data")
async def get_project_data(data: ProjectDataInput):
    file_path = get_local_file_path(data.file_path)
    object_name = data.object_name

    current_file_path = get_current_blend_file_path()
    if current_file_path != file_path:
        load_blend_file(file_path)
    
    data = get_mesh_data(object_name)
    return data

@app.post("/project/render")
async def render_project(data: RenderProjectInput):
    file_path = get_local_file_path(data.file_path)
    object_name = data.object_name
    modifiers = data.modifiers

    current_file_path = get_current_blend_file_path()
    if current_file_path != file_path:
        load_blend_file(file_path)

    try:
        out_path = render_object(object_name, modifiers, OutputFormat.GLB)
        return {"out_path": out_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to render project: {e}")
    


