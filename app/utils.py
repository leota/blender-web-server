import bpy
import logging
from typing import List


logging.basicConfig(level=logging.INFO)

def get_scene_mesh_names() -> List[str]:
    try:
        meshes = []
        scene = bpy.context.scene

        for obj in scene.objects:
            if obj.type == 'MESH':
                meshes.append(obj.name)

        return meshes
    except Exception as e:
        logging.error(f"Failed to get meshes: {e}", exc_info=True)
        raise Exception(f"Failed to get meshes: {e}")

def load_blend_file(blend_file_path: str):
    """
    Load a .blend file into the current scene.
    
    :param blend_file_path: The path to the .blend file.
    """
    try:
        # Load the .blend file data
        with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
            # Here you can specify what to load e.g., objects, materials etc.
            data_to.objects = [name for name in data_from.objects]

        # Link the objects to the current scene
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
    except Exception as e:
        raise Exception(f"Failed to load .blend file: {e}")
