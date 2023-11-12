import os
import sys
import bpy
import json


class Parameter:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type


class Modifier:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters


class BlenderInput:
    def __init__(self, object_name, modifiers):
        self.object_name = object_name
        self.modifiers = modifiers


def parse_blender_input(json_data):
    data = json.loads(json_data)
    object_name = data["object_name"]
    modifiers = []

    for mod_data in data["modifiers"]:
        mod_name = mod_data["name"]
        parameters = []

        for param_data in mod_data["parameters"]:
            param_name = param_data["name"]
            param_value = param_data["value"]
            param_type = param_data["type"]
            parameter = Parameter(param_name, param_value, param_type)
            parameters.append(parameter)

        modifier = Modifier(mod_name, parameters)
        modifiers.append(modifier)

    blender_input = BlenderInput(object_name, modifiers)
    return blender_input


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
        console_write(f"Unsupported parameter type: {parameter_type}")
        return value


def console_get():
    for area in bpy.context.screen.areas:
        if area.type == "CONSOLE":
            for space in area.spaces:
                if space.type == "CONSOLE":
                    return area, space
    return None, None


def console_write(text):
    area, space = console_get()
    if space is None:
        return

    context = bpy.context.copy()
    context.update(
        dict(
            space=space,
            area=area,
        )
    )
    for line in text.split("\n"):
        bpy.ops.console.scrollback_append(context, text=line, type="OUTPUT")


def update_object(data: BlenderInput) -> bool:
    # Get the object by name
    obj = bpy.data.objects.get(data.object_name)
    if obj is None:
        console_write(f"Object not found: {data.object_name}")
        return

    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Go through each modifier
    for mod in data.modifiers:
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


def render_object_to_glb(object_name, out_dir, out_file_name):
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


def load_json_and_render_object(json_file_path):
    with open(json_file_path, "r") as file:
        json_data = file.read()

    blender_input = parse_blender_input(json_data)
    update_result = update_object(blender_input)

    if update_result:
        json_file_name = os.path.basename(json_file_path)
        json_file_name_without_ext = os.path.splitext(json_file_name)[0]
        render_object_to_glb(blender_input.object_name, "/tmp/blender", json_file_name_without_ext)
    else:
        console_write("Error occurred during object update. Rendering skipped.")

# Execute script
json_file_path = sys.argv[5]
load_json_and_render_object(json_file_path)
