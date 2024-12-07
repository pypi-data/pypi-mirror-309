# flake8: noqa
import os
import os.path as osp

from dotenv import load_dotenv

from .authenticate import authenticate  # noqa

env_file = osp.join(osp.dirname(__file__), '.env')
if osp.exists(env_file):
    load_dotenv(env_file)

if not os.getenv('VINZ_URL'):
    raise RuntimeError(f'Missing required environment variable: VINZ_URL')
