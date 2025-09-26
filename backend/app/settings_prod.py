from app.settings import *
import os

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "thss",
        "USER": "root",
        "PASSWORD": os.environ.get("MYSQL_ROOT_PASSWORD", ""),
        "HOST": "mysql",
        "PORT": "3306",
    }
}
