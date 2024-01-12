. fastapi_env/bin/activate

SITE_PACKAGES_PATH=$(python3 -c "import site; print(site.getsitepackages()[0])") blender -b server.blend --python _blender_script.py