import logging
import os

from furl import furl
import requests

from . import utils

logger = logging.getLogger(__name__)


def authenticate(env_name='ATLASAI_TOKEN'):
    """
     Authenticate with Vinz

     Returns an OAuth2 Access Token

     If `env_name` provided, the Access Token will be saved
     to the named environment variable

     #### Usage

     ```python
     from atlasai.vinz import client

     token = client.authenticate(<OPTIONAL_ENV_VARIABLE_NAME>)
     ```
     """

    f = furl(utils.get_url())
    f.path = 'api/token'
    url = f.url
    headers = {}
    utils.include_authorization(url, headers)

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    token = data['access_token']

    if env_name:
        os.environ[env_name] = token

    user_id = data.get('email') or data.get('sub') or 'AtlasAI Employee'
    os.environ['LOGNAME'] = user_id

    return token
