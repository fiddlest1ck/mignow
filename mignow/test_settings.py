import os
from mignow.settings import *  # noqa: F401 F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),  # noqa: F405
    }
}
