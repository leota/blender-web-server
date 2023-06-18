FROM linuxserver/blender:latest

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install fastapi uvicorn numpy python-dotenv

ENV BLENDER_PROJECT_PATH="/projects/table.blend"

RUN mkdir /tmp/blender

WORKDIR /app

COPY ./app /app
COPY ./projects /projects

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
