import bpy
from typing import List

def get_scene_mesh_names() -> List[str]:
    meshes = []
    scene = bpy.context.scene

    for obj in scene.objects:
        if obj.type == 'MESH':
            meshes.append(obj.name)

    return meshes
