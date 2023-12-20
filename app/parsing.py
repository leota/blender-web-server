import bpy
import re

from classes import ParameterType

ALLOWED_PARAMETER_TYPES = ["FLOAT", "INT", "BOOLEAN", "ENUM", "VALUE"]

def format_number(value):
    if isinstance(value, float):
        if value > 1000:
            return 150.00
        return round(value, 2)
    elif isinstance(value, int):
        if value > 1000:
            return 150
        return value
    else:
        raise Exception(f"Invalid value type: {type(value)}")
    

def parse_parameter_type(prop_type) -> ParameterType:
    if prop_type == "FLOAT" or prop_type == "VALUE":
        return ParameterType.Float
    elif prop_type == "INT":
        return ParameterType.Int
    elif prop_type == "BOOLEAN":
        return ParameterType.Boolean
    elif prop_type == "ENUM":
        return ParameterType.Menu
    else:
        return ParameterType.String

    
def format_prop_value(prop, prop_name: str):
    if hasattr(prop, prop_name) and prop.type in ["FLOAT", "VALUE", "INT"]:
        return format_number(getattr(prop, prop_name))
    elif hasattr(prop, prop_name) and prop.type in ["BOOLEAN"]:
        if getattr(prop, prop_name) == "True":
            return "true"
        else:
            return "false"
    else:
        return None
    

def get_enum_items_from_rna(rna, prop_name):
    enum_items = []
    
    prop_rna = rna.bl_rna.properties.get(prop_name)
    if prop_rna and prop_rna.type == 'ENUM':
        for item in prop_rna.enum_items:
            enum_items.append({"label": item.name, "value": item.identifier})
    
    return enum_items

def format_geometry_nodes_modifier_default_value(mod, prop):
    # Format default value for Geometry Nodes inputs
    if hasattr(mod, prop.identifier) and prop.type in ["FLOAT", "VALUE", "INT"]:
        return str(format_number(mod[prop.identifier]))
    elif hasattr(mod, prop.identifier) and prop.type in ["BOOLEAN"]:
        return str(mod[prop.identifier]).lower()
    elif hasattr(mod, prop.identifier) and prop.type in ["ENUM"]:
        return str(mod[prop.identifier])
    else:
        return None

def format_property_data_geometry_nodes(mod, prop):
    # Format data for Geometry Nodes inputs
    return {
        "label": str(prop.name),
        "name": str(prop.identifier),
        "path": f"{mod.name}/{prop.identifier}",
        "type": parse_parameter_type(str(prop.type)),
        "min": format_prop_value(prop, "min_value"),
        "max": format_prop_value(prop, "max_value"),
        "defaultValue": format_geometry_nodes_modifier_default_value(mod, prop),
        "options": []
    }

def format_regular_modifier_default_value(mod, prop):
    # Format default value for regular modifiers
    if hasattr(mod, prop.identifier) and prop.type in ["FLOAT", "VALUE", "INT"]:
        return str(format_number(getattr(mod, prop.identifier)))
    elif hasattr(mod, prop.identifier) and prop.type in ["BOOLEAN"]:
        return str(getattr(mod, prop.identifier)).lower()
    elif hasattr(mod, prop.identifier) and prop.type in ["ENUM"]:
        return str(getattr(mod, prop.identifier))
    else:
        return None

def format_property_data_regular_modifier(mod, prop):
    # Format data for regular modifiers
    return {
        "label": str(prop.name),
        "name": str(prop.identifier),
        "path": f"{mod.name}/{prop.identifier}",
        "type": parse_parameter_type(str(prop.type)),
        "min": format_prop_value(prop, "hard_min"),
        "max": format_prop_value(prop, "hard_max"),
        "defaultValue": format_regular_modifier_default_value(mod, prop),
        "options": get_enum_items_from_rna(mod, prop.identifier)
    }

def process_modifier(mod):
    mod_data = {
        "name": str(mod.name),
        "label": str(mod.name),
        "path": str(mod.name),
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