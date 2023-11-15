FROM linuxserver/blender:latest

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install fastapi uvicorn numpy python-dotenv

RUN mkdir /tmp/blender

WORKDIR /app

COPY ./app /app
COPY ./projects /projects

EXPOSE 8000

# blender -b server.blend --python _blender_script.py
ENTRYPOINT ["blender", "/app/server.blend", "--background", "--python", "/app/_blender_script.py"]