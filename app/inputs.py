from pydantic import BaseModel

class ImportProjectInput(BaseModel):
    file_path: str