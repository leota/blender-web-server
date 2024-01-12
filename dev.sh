virtualenv fastapi_env
source fastapi_env/bin/activate
pip install -r requirements.txt

mkdir /tmp/projects
cd app

SITE_PACKAGES_PATH=$(python -c "import site; print(site.getsitepackages()[0])") blender -b server.blend --python _blender_script.py

