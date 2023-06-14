import os
import sys
import bpy


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


def update_modifier_parameter(object_name, modifier_name, parameter_name, parameter_value):
    # Get the object by name
    obj = bpy.data.objects.get(object_name)
    if obj is None:
        console_write(f"Object not found: {object_name}")
        return

    # Check if the modifier exists
    if modifier_name not in obj.modifiers:
        console_write(f"Modifier not found: {modifier_name}")
        return

    modifier = obj.modifiers[modifier_name]

    # Check if the modifier is a Geometry Nodes modifier
    if modifier.type == "NODES":
        # Handle Geometry Nodes parameters
        obj.modifiers[modifier_name][parameter_name] = parameter_value
        console_write(f"Modified Geometry Node input parameter: {modifier_name} - {parameter_name} = {parameter_value}")
    else:
        # Handle other types of parameters
        if hasattr(modifier, parameter_name):
            setattr(modifier, parameter_name, parameter_value)
            console_write(f"Modified parameter: {modifier_name} - {parameter_name} = {parameter_value}")
        else:
            console_write(f"Parameter not found: {parameter_name}")

    bpy.context.object.data.update()


def render_object_to_glb(object_name, out_dir):
    # Select the object by name
    bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
    bpy.data.objects[object_name].select_set(True)

    # Apply all modifiers to the object
    bpy.ops.object.convert(target="MESH")

    # Set the output path and filename for the .glb file
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    output_path = os.path.join(out_dir, object_name + ".glb")
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


# Example usage
# object_name = "Procedural Table GN"
# modifier_name = "Bevel"
# parameter_name = "width"
# parameter_value = 1.0

# Read command-line arguments
object_name = sys.argv[5]
modifier_name = sys.argv[6]
parameter_name = sys.argv[7]
parameter_value = 1.0

print("object_name: ", object_name)
print("modifier_name: ", modifier_name)
print("parameter_name: ", parameter_name)
print("parameter_value: ", parameter_value)

update_modifier_parameter(object_name, modifier_name, parameter_name, parameter_value)
render_object_to_glb(object_name, "/app/projects/output/")

# Usage
# blender /Users/leonardo/workspace/polygona/blender-server/projects/table.blend --background --python app/blender_script.py "Procedural Table GN" "Bevel" "width" 1.0