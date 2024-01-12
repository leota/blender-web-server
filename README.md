# blender-engine

## Run locally
- Copy `./app/env-example` to `./app/.env` and add teh required variables.
- Run `./dev.sh`


## Docker

### Build and run
```
docker build -t blender-container .
docker run -it --rm -p 8080:8080 blender-container
```
