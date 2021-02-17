import appdirs
import os
import pathlib
import sys

log = lambda msg: print(f'Serverless: \x1b[0;33m{msg}\x1b[0m')

[org, app, chromium_artifact_str_path, requirements_artifact_str_path] = [*sys.argv[1:]]
user_cache_path = pathlib.Path(appdirs.user_cache_dir(app, org))

chromium_artifact_path = pathlib.Path(chromium_artifact_str_path)
chromium_artifact_cache_path = user_cache_path.joinpath(chromium_artifact_path.name)

requirements_artifact_path = pathlib.Path(requirements_artifact_str_path)
requirements_artifact_cache_path = user_cache_path.joinpath(requirements_artifact_path.name)

if not user_cache_path.exists():
  user_cache_path.mkdir(0o755, True)

if chromium_artifact_cache_path.exists() and requirements_artifact_cache_path.exists():
  log(f'Using cached layer artifacts: {user_cache_path}')
else:
  log(f'Packaging layer artifacts: {user_cache_path}')

  docker_image = f'{org}/{app}-layer-artifacts'

  os.system(f'docker build --no-cache -t {docker_image} .')
  os.system(f'''docker run --rm -v {user_cache_path}:/data {docker_image} \\
    cp {chromium_artifact_path.name} {requirements_artifact_path.name} /data''')

chromium_artifact_cache_path.link_to(chromium_artifact_path)
requirements_artifact_cache_path.link_to(requirements_artifact_path)
