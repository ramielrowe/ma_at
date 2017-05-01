import json
import os

DATA_FILE = os.getenv('DATA_FILE', 'ma_at.json')


def load():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, 'r') as fp:
        return json.load(fp)


def save():
    with open(DATA_FILE, 'w') as fp:
        json.dump(DATA, fp)


DATA = load()


def get(key, default=None):
    if default is None:
        default = {}
    return DATA.setdefault(key, default)
