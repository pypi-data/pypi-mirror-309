# bob3 client for python

This is a python client for the bob3 API endpoints. It is lightweight utility to provide
easier access to the API endpoints.

## Installation

```bash
pip install bob3client
```

## Usage

To authenticate against the API you must have a private RSA key file available. This key file
is used to sign the JWT token that is used to authenticate against the API.

Authentication works in such a way that you first register app in the workspace and provide
permissions to it in bob3. There you will need to provide public key of the RSA key pair that
you will use to sign the JWT token. There you also acquire app_id that you will use.

To make easier authentication `bob3client` provides a function `get_auth_token` that will
do all authentication job for you and return already a token that you can use to authenticate
to bob3 API. You will not need to sign JWT token yourself or call `POST /auth` endpoint.

```python
import bob3client

# Acquire an authorization token
# workspace: the workspace name to authorize against
# app_id: the application id that was created in the workspace (see bob3 documentation)
# private_rsa_key_path: the path to the private RSA key file
# Token will expire in 60 minutes by default, to change this use the expire parameter
token = bob3client.get_auth_token('workspace', 'app_id', 'private_rsa_key_path')

# Now you must provide the token in Authorization header to access the API endpoints
# Example using requests library
import requests
headers = {"Authorization": token}
# Get all projects in the workspace where the app is authorized
response = requests.get(bob3client.BOB3_PROD_URL + 'projects', headers=headers)
print(response.json())
```

To get API documentation fetch simply bob3client.BOB3_PROD_URL path in your favorite browser.
