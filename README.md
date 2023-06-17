# blender-engine

## Development
`cd app && uvicorn main:app --reload`


## Docker
```
docker build -t blender-container .
docker run -it --rm -p 8000:8000 -v /Users/leonardo/workspace/polygona/blender-server/projects:/app/projects blender-container
```