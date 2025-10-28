import logging
import requests
import time
import os
from datetime import datetime, timedelta
from google.cloud import firestore, secretmanager
from google.auth import default
from google.api_core.exceptions import NotFound

db = firestore.Client()
_, PROJECT_ID = default()
SECRET_ID = "INSTAGRAM_ACCESS_TOKEN"
SECRET_PARENT = f"projects/{PROJECT_ID}"
SECRET_NAME = f"{SECRET_PARENT}/secrets/{SECRET_ID}"
SECRET_VERSION_NAME = f"{SECRET_NAME}/versions/latest"


def get_refresh_info():
    doc = db.collection("tokens").document("instagram").get()
    if doc.exists:
        return doc.to_dict()
    return {"last_refreshed": None}

def update_refresh_info():
    db.collection("tokens").document("instagram").set({
        "last_refreshed": datetime.utcnow().isoformat()
    })

def maybe_refresh_token():
    info = get_refresh_info()
    last = info.get("last_refreshed")
    if not last:
        logging.info("No previous refresh recorded, refreshing now.")
        do_refresh()
        update_refresh_info()
        return

    last_dt = datetime.fromisoformat(last)
    days_elapsed = (datetime.utcnow() - last_dt).days

    if days_elapsed >= 45:
        logging.info(f"{days_elapsed} days since last refresh — refreshing token.")
        do_refresh()
        update_refresh_info()
    else:
        logging.info(f"Only {days_elapsed} days since last refresh — skipping refresh.")

def do_refresh():
    long_token = get_token()
    if not long_token:
        logging.error("No token found in env vars.")
        return
    url = f"https://graph.instagram.com/refresh_access_token"
    params = {
        "grant_type": "ig_refresh_token",
        "access_token": long_token,
    }
    r = requests.get(url, params=params)
    data = r.json()
    logging.info(f"Refreshed token response: {data}")
    new_token = data.get("access_token")
  
    if new_token:
        # Store only in Secret Manager, not Firestore
        sm = secretmanager.SecretManagerServiceClient()
        # Ensure the secret id exists
        current_secret = get_token()
        logging.info(f"Overwriting most recent secret: {current_secret}")
        sm.add_secret_version(parent=SECRET_NAME, payload={"data": new_token.encode("utf-8")})

def get_token():
    access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", 0)

    # access_token available in dev
    if access_token:
        logging.info("Local testing: Using developer secret. This does not refresh automatically")
        return access_token

    sm = secretmanager.SecretManagerServiceClient()

    try:
        # Ensure the secret exists
        response = sm.access_secret_version(name=SECRET_VERSION_NAME)
        return response.payload.data.decode("utf-8")
    except NotFound:
        logging.info("Secret not found — creating it now.")
        sm.create_secret(
            parent=SECRET_PARENT,
            secret_id=SECRET_ID,
            secret=secretmanager.Secret(
                replication=secretmanager.Replication(
                    automatic=secretmanager.Replication.Automatic()
                )
            ),
        )
        return ""

def wait(seconds: int):
    """Sleep for the given number of seconds."""
    time.sleep(seconds)


def is_upload_successful(retry_count: int, check_status_uri: str) -> bool:
    """
    Polls the video upload status endpoint until the upload is marked as finished
    or until retries are exhausted.

    Args:
        retry_count (int): current retry attempt
        check_status_uri (str): URL to check the upload container status

    Returns:
        bool: True if upload completed successfully, False otherwise
    """
    if retry_count > 30:
        return False

    try:
        response = requests.get(check_status_uri)
        logging.debug(f"Checking if upload is successful. Response details: {response.json()}")
        response.raise_for_status()
        data = response.json()

        # Meta returns fields like {"status_code": "FINISHED"}
        if data.get("status_code") != "FINISHED":
            seconds_to_wait = 3
            logging.info(f"Video not uploaded yet. Waiting {seconds_to_wait} seconds")
            wait(seconds_to_wait)  # wait 3 seconds before retry
            return is_upload_successful(retry_count + 1, check_status_uri)

        return True

    except requests.RequestException as e:
        raise e


# Example usage:
# check_status_uri = "https://graph.facebook.com/v21.0/{container_id}?fields=status_code&access_token={token}"
# success = is_upload_successful(0, check_status_uri)
# print("Upload completed:", success)
