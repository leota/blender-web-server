import bpy
import re

from classes import ParameterType

ALLOWED_PARAMETER_TYPES = ["FLOAT", "INT", "BOOLEAN", "ENUM", "VALUE"]

def format_float(value):
    float_string = "{:.2e}".format(value)
    float_string = re.sub(r"(\d+\.\d+)[eE].*", r"\1", float_string)
    return float_string

def get_enum_items_from_rna(rna, prop_name):
    enum_items = []
    
    prop_rna = rna.bl_rna.properties.get(prop_name)
    if prop_rna and prop_rna.type == 'ENUM':
        for item in prop_rna.enum_items:
            enum_items.append({"label": item.name, "value": item.identifier})
    
    return enum_items

def format_property_data_geometry_nodes(mod, prop):
    # Format data for Geometry Nodes inputs
    return {
        "label": str(prop.name),
        "name": str(prop.identifier),
        "path": f"{mod.name}/{prop.identifier}",
        "type": str(prop.bl_label),
        "min": format_float(prop.min_value)
        if hasattr(prop, "min_value") and prop.type in ["FLOAT", "VALUE"]
        else str(prop.min_value)
        if hasattr(prop, "min_value")
        else "N/A",
        "max": format_float(prop.max_value)
        if hasattr(prop, "max_value") and prop.type in ["FLOAT", "VALUE"]
        else str(prop.max_value)
        if hasattr(prop, "max_value")
        else "N/A",
        "defaultValue": format_float(prop.default_value)
        if hasattr(prop, "default_value") and prop.type in ["FLOAT", "VALUE"]
        else str(prop.default_value)
        if hasattr(prop, "default_value")
        else "N/A",
        "options": []
    }

def format_property_data_regular_modifier(mod, prop):
    # Format data for regular modifiers
    return {
        "label": str(prop.name),
        "name": str(prop.identifier),
        "path": f"{mod.name}/{prop.identifier}",
        "type": str(prop.type),
        "min": format_float(prop.hard_min)
        if hasattr(prop, "hard_min") and prop.type in ["FLOAT", "VALUE"]
        else str(prop.hard_min)
        if hasattr(prop, "hard_min")
        else "N/A",
        "max": format_float(prop.hard_max)
        if hasattr(prop, "hard_max") and prop.type in ["FLOAT", "VALUE"]
        else str(prop.hard_max)
        if hasattr(prop, "hard_max")
        else "N/A",
        "defaultValue": format_float(prop.default)
        if hasattr(prop, "default") and prop.type in ["FLOAT", "VALUE"]
        else str(prop.default)
        if hasattr(prop, "default")
        else "N/A",
        "options": get_enum_items_from_rna(mod, prop.identifier)
    }

def process_modifier(mod):
    mod_data = {
        "name": str(mod.name),
        "label": str(mod.name),
        "mod_type": str(mod.type),
        "type": str(ParameterType.Folder.value),
        "children": []
    }

    if mod.type == "NODES" and mod.node_group:
        # Handle Geometry Nodes
        for prop in mod.node_group.inputs:
            if prop.type in ALLOWED_PARAMETER_TYPES:
                prop_data = format_property_data_geometry_nodes(mod, prop)
                mod_data["children"].append(prop_data)
    else:
        # Handle regular modifiers
        for prop in mod.bl_rna.properties:
            if not prop.is_readonly and prop.type in ALLOWED_PARAMETER_TYPES:
                prop_data = format_property_data_regular_modifier(mod, prop)
                mod_data["children"].append(prop_data)

    return mod_data

def get_object_by_name(name):
    """
    Get an object from the current scene by its name.

    Args:
    name (str): The name of the object.

    Returns:
    bpy.types.Object: The Blender object with the given name, or None if not found.
    """
    # Check if the object exists in the current scene
    if name in bpy.data.objects:
        return bpy.data.objects[name]
    else:
        print(f"No object found with name: {name}")
        return None


def get_mesh_data(name: str):
    object = get_object_by_name(name)
    mod_list = object.modifiers

    data = {
        "name": str(object.name),
        "modifiers": [],
        "info": {
            "blender_version": bpy.app.version_string
        }
    }

    for mod in mod_list:
        mod_data = process_modifier(mod)
        data["modifiers"].append(mod_data)

    return data