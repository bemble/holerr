import os

def get_app_version():
    return os.getenv("APP_VERSION", "local")