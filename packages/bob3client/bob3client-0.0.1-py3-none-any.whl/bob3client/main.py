"""bob3 client interaction methods and classes."""

import json
import time
import urllib.request

from joserfc import jwt
from joserfc.jwk import RSAKey

BOB3_PROD_URL = "https://bob-3-0-3061-59a6-be-production-dg7gvejxcq-ew.a.run.app/"
BOB3_STAGING_URL = "https://bob-3-0-3061-59a6-be-staging-dg7gvejxcq-ew.a.run.app/"
BOB3_TEST_URL = "https://bob-3-0-3061-59a6-be-test-dg7gvejxcq-ew.a.run.app/"


class Bob3ClientError(Exception):
    """Generic Bob3 client error."""


def invalid_base_url(base_url):
    """Raise error for invalid base url."""
    msg = f"Invalid base url: {base_url}"
    msg += " use BOB3_PROD_URL, BOB3_STAGING_URL or BOB3_TEST_URL"
    raise Bob3ClientError(msg)


def get_jwt_token(app_id, key_path, expire=60):
    """Generate JWT token.

    Args:
    app_id (str): App name which has access to workspace and owns private key
    key_path (str): Path to private key file.
    expire (int): Token expiration time in minutes.
    """
    now = time.time()
    expire = now + expire * 60
    with open(key_path, "r") as f:
        private_key = f.read()
    key = RSAKey.import_key(private_key)
    return jwt.encode({"alg": "RS256"}, {"sub": app_id, "iat": now, "exp": expire}, key)


def get_auth_payload(workspace, app_id, private_key_path, expire):
    """Get auth payload.

    Args:
    workspace (str): Workspace name to login to.
    app_id (str): App name which has access to workspace and owns private key
    private_key_path (str): Path to RSA private key file.
    expire (int): Token expiration time in minutes.
    """
    payload = {
        "method": {
            "mode": "rsa",
            "token": get_jwt_token(app_id, private_key_path, expire),
        },
        "workspace": workspace,
    }
    return json.dumps(payload).encode("utf-8")


def get_auth_token(
    workspace, app_id, rsa_private_key_path, base_url=BOB3_PROD_URL, expire=60
):
    """Get auth token from bob3 to use in all requests.

    Args:
    workspace (str): Workspace name to login to.
    app_id (str): App id which has access to workspace and owns private key
    rsa_private_key_path (str): Path to RSA private key file.
    base_url (str): Bob3 base url, BOB3_PROD_URL, BOB3_STAGING_URL or BOB3_TEST_URL.
    expire (int): Token expiration time in minutes.
    """
    try:
        req = urllib.request.Request(
            base_url + "auth",
            method="POST",
            data=get_auth_payload(workspace, app_id, rsa_private_key_path, expire),
        )
    except ValueError:
        invalid_base_url(base_url)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))["token"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            invalid_base_url(base_url)
        if e.code in [422, 500]:
            msg = e.read().decode("utf-8")
            msg = json.loads(msg)
            raise Bob3ClientError(msg[0])
        raise e
