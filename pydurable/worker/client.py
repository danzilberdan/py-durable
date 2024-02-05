import os
from temporalio.client import Client


API_KEY_ENV = "API_KEY"
API_KEY_MD_KEY = "durable_api_key"
TEMPORAL_URL = "3.215.127.194:7234"
# TEMPORAL_URL = "localhost:7234"


async def get_client(api_key: str=None) -> Client:
    if not api_key and API_KEY_ENV in os.environ:
        api_key = os.environ[API_KEY_ENV]

    if not api_key:
        raise KeyError("Durable SDK could not find API key")
    
    print('Connecting to ' + TEMPORAL_URL)

    return await Client.connect(TEMPORAL_URL, namespace='', rpc_metadata={
        API_KEY_MD_KEY: api_key
    })
