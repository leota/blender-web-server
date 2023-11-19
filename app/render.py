import os
import bpy
import logging
from typing import List
from classes import Modifier, OutputFormat
from utils import generate_random_string
from config import Settings

env = Settings()
logging.basicConfig(level=logging.INFO)

def render_object(object_name: str, modifiers: List[Modifier], output_format: OutputFormat):
    update_result = update_object(object_name, modifiers)
    if update_result:
        output_file_name = f"{object_name}_{generate_random_string()}"
        if output_format == OutputFormat.GLB:
            return render_object_to_glb(object_name, env.OUTPUT_FOLDER, output_file_name)
        else:
            raise Exception(f"Unsupported output format: {output_format}")
    else:
        raise Exception("Failed to update object")

def update_object(object_name: str, modifiers: List[Modifier]) -> bool:
    # Get the object by name
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        logging.error(f"Object not found: {object_name}")
        return

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Go through each modifier
    for mod in modifiers:
        # Check if the modifier exists
        if mod.name not in obj.modifiers:
            raise Exception(f"Modifier not found: {mod.name}")

        modifier = obj.modifiers[mod.name]

        # Go through each parameter
        for param in mod.parameters:
            # Check if the modifier is a Geometry Nodes modifier
            if modifier.type == "NODES":
                # Handle Geometry Nodes parameters
                obj.modifiers[mod.name][param.name] = convert_parameter_value(param.value, param.type)
            else:
                # Handle other types of parameters
                if hasattr(modifier, param.name):
                    setattr(modifier, param.name, convert_parameter_value(param.value, param.type))
                else:
                    raise Exception(f"Parameter not found: {param.name} in modifier {mod.name}")

    bpy.context.object.data.update()
    return True

def convert_parameter_value(value: str, parameter_type: str):
    if parameter_type == "FLOAT" or parameter_type == "VALUE":
        return float(value)
    elif parameter_type == "INT":
        return int(value)
    elif parameter_type == "BOOLEAN":
        return value.lower() == "true"
    elif parameter_type == "ENUM":
        return value  # Assuming the value is already a valid enum value
    else:
        logging.warn(f"Unsupported parameter type: {parameter_type}")
        return value

def render_object_to_glb(object_name: str, out_dir: str, out_file_name: str):
    # Select the object by name
    bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
    bpy.data.objects[object_name].select_set(True)

    # Set the output path and filename for the .glb file
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    output_path = os.path.join(out_dir, out_file_name + ".glb")
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = output_path

    # Enable Draco compression for the .glb file
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_colors=True,
        export_texcoords=True,
        export_normals=True,
        export_materials="EXPORT",
        export_cameras=False,
        export_lights=False,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
    )

    # Deselect the object
    bpy.data.objects[object_name].select_set(False)

    return output_path
