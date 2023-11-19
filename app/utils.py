import bpy
import logging
import random
import string
from typing import List
from urllib.parse import urlparse
from pathlib import Path
from digitalocean.s3 import download_file_from_space, client
from config import Settings

env = Settings()
logging.basicConfig(level=logging.INFO)


def generate_random_string(length=8):
    """
    Generate a random alphanumeric string.

    Args:
    length (int): Length of the generated string. Default is 8.

    Returns:
    str: The generated random string.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def is_url(string):
    parsed = urlparse(string)
    return all([parsed.scheme, parsed.netloc])

def file_exists(file_path: str):
    file = Path(file_path)
    return file.is_file()

def get_filename_from_url(url: str):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = path.split('/')[-1]
    return filename

    
def get_local_file_path(url: str):
    """
    Get the local file path of a file.

    Args:
    file_path (str): The file path.

    Returns:
    str: The local file path.
    """
    if is_url(url):
        local_file_path = f"{env.PROJECTS_FOLDER}/{get_filename_from_url(url)}"
        if file_exists(local_file_path):
            return local_file_path
        else:
            file_path_without_base_url = url.split(
                f"https://{env.DO_SPACES_BUCKET_NAME}.{env.DO_SPACES_REGION}.digitaloceanspaces.com/"
            )[-1]
            download_file_from_space(
                client,
                env.DO_SPACES_BUCKET_NAME,
                file_path_without_base_url,
                local_file_path,
            )
            return local_file_path
    else:
        return url


def get_current_blend_file_path():
    """
    Get the path of the currently opened Blender file.

    Returns:
    str: The file path of the current .blend file, or an empty string if no file is loaded.
    """
    file_path = bpy.data.filepath
    if file_path:
        return file_path
    else:
        return None

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

def import_blend_file(blend_file_path: str):
    """
    Import a .blend file into the current scene.
    
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
    
def load_blend_file(blend_file_path: str):
    """
    Open a .blend file, replacing the current scene.
    Args:
    file_path (str): The path to the .blend file.
    """
    try:
        bpy.ops.wm.open_mainfile(filepath=blend_file_path)
        logging.info(f"Opened file: {blend_file_path}")
    except Exception as e:
        logging.error(f"Failed to open file: {e}", exc_info=True)
        raise Exception(f"Failed to open file: {e}")
    
def rename_object(obj_name, new_name):
    """
    Rename an object in the Blender scene.

    Args:
    obj_name (str): The current name of the object.
    new_name (str): The new name to be assigned to the object.

    Returns:
    str: The new name of the object, or None if the object is not found.
    """
    if obj_name in bpy.data.objects:
        bpy.data.objects[obj_name].name = new_name
        return bpy.data.objects[new_name].name
    else:
        logging.info(f"Object '{obj_name}' not found.")
        return None

