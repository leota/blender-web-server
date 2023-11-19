FROM linuxserver/blender:latest

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install fastapi uvicorn numpy python-dotenv pydantic-settings boto3

RUN mkdir /tmp/output
RUN mkdir /tmp/projects

WORKDIR /app

COPY ./app /app

EXPOSE 8000

# blender -b server.blend --python _blender_script.py
ENTRYPOINT ["blender", "/app/server.blend", "--background", "--python", "/app/_blender_script.py"]