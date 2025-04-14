import json
import hashlib
import os

USERS_FILE = "users.json"

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE):
        default_users = {
            "admin": {
                "password": hash_password("admin123"),
                "role": "admin"
            },
            "user1": {
                "password": hash_password("user123"),
                "role": "readonly"
            }
        }
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f)
        print("Created default users.json with admin and read-only users.")
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def authenticate(username, password):
    users = load_users()
    if username in users:
        stored_hash = users[username]['password']
        entered_hash = hash_password(password)
        if stored_hash == entered_hash:
            return users[username]['role']
    return None