"""Bob3 API client library.

Library provides helpfull classes and methods to interact with Bob3 API.


Usage examples:

```shell
pip install bob3client
```

>>> # Acquire Authorization token
>>> import bob3client
>>> token = bob3client.get_auth_token("workspace", "app_id", "private_rsa_key_path")

Using requests:

```shell
pip install requests
```

>>> import requests
>>> headers = {"Authorization": token}
>>> response = requests.get(bob3client.BOB3_PROD_URL + "projects", headers=headers)
>>> print(response.json())
>>> response = requests.post(bob3client.BOB3_PROD_URL + "projects", headers=headers, json={"name": "My project"})
>>> print(response.json())
>>> my_project_id = response.json()["id"]
>>> response = requests.get(bob3client.BOB3_PROD_URL + f"projects/{my_project_id}", headers=headers)
>>> print(response.json())
>>> response = requests.put(bob3client.BOB3_PROD_URL + f"projects/{my_project_id}", headers=headers, json={"name": "My project Edited"})
>>> print(response.json())
>>> response = requests.delete(bob3client.BOB3_PROD_URL + f"projects/{my_project_id}", headers=headers)
>>> print(response.json())

"""

from .main import get_auth_token, BOB3_PROD_URL, BOB3_STAGING_URL, BOB3_TEST_URL

__version__ = "0.0.1"

__all__ = ["get_auth_token", "BOB3_PROD_URL", "BOB3_STAGING_URL", "BOB3_TEST_URL"]
