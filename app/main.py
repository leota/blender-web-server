from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import os
import json
import hashlib
import subprocess
from dotenv import load_dotenv


class Parameter(BaseModel):
    name: str
    value: str
    type: str


class Modifier(BaseModel):
    name: str
    parameters: List[Parameter]


class BlenderInput(BaseModel):
    object_name: str
    modifiers: List[Modifier]

load_dotenv()
BLENDER_PROJECT_PATH = os.getenv("BLENDER_PROJECT_PATH")
app = FastAPI()


@app.post("/render")
async def set_data(data: BlenderInput):
    # convert data to dict and then to json
    data_as_json = json.dumps(data.dict())

    # create a hash of the json data
    hash_object = hashlib.md5(data_as_json.encode())
    hex_dig = hash_object.hexdigest()

    # save json to file with hash as filename
    json_file_path = os.path.abspath(f"/tmp/blender/{hex_dig}.json")
    with open(json_file_path, "w") as file:
        file.write(data_as_json)

    blender_command = [
        "blender",
        BLENDER_PROJECT_PATH,
        "--background",
        "--python",
        "blender_script.py",
        json_file_path,
    ]
    subprocess.run(blender_command)

    return {"message": "Data successfully received and stored", "filename": f"{hex_dig}.json"}

