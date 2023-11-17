from enum import Enum
from pydantic import BaseModel

class ParameterType(Enum):
    Folder = 'Folder'
    String = 'String'
    Boolean = 'Boolean'
    Toggle = 'Toggle'
    Int = 'Int'
    Float = 'Float'
    Menu = 'Menu'

class ImportProjectInput(BaseModel):
    file_path: str

class LoadProjectInput(BaseModel):
    file_path: str

class ProjectDataInput(BaseModel):
    file_path: str
    object_name: str