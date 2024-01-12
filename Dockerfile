FROM linuxserver/blender:3.6.5-ls78

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install fastapi uvicorn numpy python-dotenv pydantic-settings boto3 'sentry-sdk[fastapi]'

RUN mkdir /tmp/output
RUN mkdir /tmp/projects

WORKDIR /app

COPY ./app /app

EXPOSE 8080

# blender -b server.blend --python _blender_script.py
ENTRYPOINT ["blender", "/app/server.blend", "--background", "--python", "/app/_blender_script.py"]