from enum import Enum
from pydantic import BaseModel

class OutputFormat(Enum):
    GLB = 'GLB'
    STL = 'STL'

class ParameterType(Enum):
    Folder = 'Folder'
    String = 'String'
    Boolean = 'Boolean'
    Toggle = 'Toggle'
    Int = 'Int'
    Float = 'Float'
    Menu = 'Menu'

class Parameter(BaseModel):
    name: str
    value: str
    type: str

class Modifier(BaseModel):
    name: str
    parameters: 'list[Parameter]'

class ImportProjectInput(BaseModel):
    file_path: str

class LoadProjectInput(BaseModel):
    file_path: str

class ProjectDataInput(BaseModel):
    file_path: str
    object_name: str

class RenderProjectInput(BaseModel):
    file_path: str
    object_name: str
    modifiers: 'list[Modifier]'
