import appdirs
import pathlib
import shutil
import sys

log = lambda msg: print(f'Serverless: \x1b[0;33m{msg}\x1b[0m')

[org, app] = [*sys.argv[1:]]
user_cache_path = pathlib.Path(appdirs.user_cache_dir(app, org))

log(f'Deleting cache directory: {user_cache_path}')

if user_cache_path.exists():
  shutil.rmtree(user_cache_path)
