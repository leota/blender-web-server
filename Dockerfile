FROM linuxserver/blender:3.6.5-ls78

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install virtualenv

RUN mkdir /tmp/output
RUN mkdir /tmp/projects

WORKDIR /app

COPY run.sh /app
COPY requirements.txt /app
RUN virtualenv fastapi_env
RUN . fastapi_env/bin/activate
RUN pip install -r requirements.txt

COPY ./app /app

EXPOSE 8080

ENTRYPOINT ./run.sh