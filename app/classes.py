from enum import Enum
from pydantic import BaseModel

class ImportProjectInput(BaseModel):
    file_path: str

class ParameterType(Enum):
    Folder = 'Folder'
    String = 'String'
    Boolean = 'Boolean'
    Toggle = 'Toggle'
    Int = 'Int'
    Float = 'Float'
    Menu = 'Menu'