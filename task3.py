import os
import hmac
import hashlib

import requests
from dotenv import load_dotenv

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Load .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

print("API Key Loaded:", API_KEY is not None)
print("Webhook Secret Loaded:", WEBHOOK_SECRET is not None)


# Retry Session
session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("http://", adapter)
session.mount("https://", adapter)


# API Call
response = session.get(
    "https://jsonplaceholder.typicode.com/users"
)

users = response.json()

print("\nFirst 5 Users:")

for user in users[:5]:
    print(
        f"{user['id']} - "
        f"{user['name']} - "
        f"{user['email']}"
    )


# Nested JSON using .get()
first_user = users[0]

city = (
    first_user
    .get("address", {})
    .get("city", "Not Available")
)

latitude = (
    first_user
    .get("address", {})
    .get("geo", {})
    .get("lat", "Not Available")
)

zip_code = (
    first_user
    .get("address", {})
    .get("zipcode", "Not Available")
)

company = (
    first_user
    .get("company", {})
    .get("name", "Not Available")
)

print("\nFirst User Details")
print("City:", city)
print("Latitude:", latitude)
print("Zip:", zip_code)
print("Company:", company)


# HMAC Verification
def verify_signature(
    payload: str,
    signature: str,
    secret: str
) -> bool:

    expected_signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        signature
    )


payload = "hello world"

valid_signature = hmac.new(
    WEBHOOK_SECRET.encode(),
    payload.encode(),
    hashlib.sha256
).hexdigest()

print("\nWebhook Results")

print(
    "Valid:",
    verify_signature(
        payload,
        valid_signature,
        WEBHOOK_SECRET
    )
)

print(
    "Tampered:",
    verify_signature(
        "tampered",
        valid_signature,
        WEBHOOK_SECRET
    )
)

print(
    "Wrong Secret:",
    verify_signature(
        payload,
        valid_signature,
        "wrong_secret"
    )
)