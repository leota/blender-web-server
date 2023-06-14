FROM linuxserver/blender:latest

# Install Python 3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install FastAPI and Uvicorn
RUN pip3 install fastapi uvicorn numpy

# Set the working directory inside the container
WORKDIR /app

# Copy the FastAPI app code into the container
COPY ./app /app

# Expose the port on which the FastAPI server will run
EXPOSE 8000

# Set the entry point command to run the FastAPI server
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
