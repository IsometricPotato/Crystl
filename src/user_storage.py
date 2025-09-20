import json
import os

USER_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'user_data', 'user_data.json')

def load_user_data():
    """
    Loads user data from the user_data.json file.
    Returns an empty dictionary if the file does not exist or is empty.
    """
    if not os.path.exists(USER_DATA_FILE) or os.stat(USER_DATA_FILE).st_size == 0:
        return {}

    with open(USER_DATA_FILE, 'r') as file:
        return json.load(file)

def save_user_data(data):
    """
    Saves the user data to the user_data.json file.
    """
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def update_user_data(data, value):
    user_data = load_user_data()

    user_data[data] = value

    save_user_data(user_data)