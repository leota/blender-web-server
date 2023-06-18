# blender-engine

## Development
`cd app && uvicorn main:app --reload`


## Docker

### Build and run
```
docker build -t blender-container .
docker run -it --rm -p 8000:8000 blender-container
```

### Upload to DO
```
docker tag blender-container registry.digitalocean.com/polygona/blender-engine
docker push registry.digitalocean.com/polygona/blender-engine
```
