import bpy
from typing import List

def get_scene_mesh_names() -> List[str]:
    meshes = []
    scene = bpy.context.scene

    for obj in scene.objects:
        if obj.type == 'MESH':
            meshes.append(obj.name)

    return meshes

def load_blend_file(blend_file_path: str):
    """
    Load a .blend file into the current scene.
    
    :param blend_file_path: The path to the .blend file.
    """
    try:
        # Load the .blend file
        with bpy.data.libraries.load(blend_file_path) as (data_from, data_to):
            data_to.objects = data_from.objects
        
        # Link the objects to the current scene
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
    except Exception as e:
        raise Exception(f"Failed to load .blend file: {e}")
