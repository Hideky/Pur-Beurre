from . import *

SECRET_KEY = '-~aO;| F;rE[??/w^zcumh(9'
DEBUG = False
ALLOWED_HOSTS = ['178.62.119.70']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'purbeurre', # le nom de notre base de données créée précédemment
        'USER': 'hideki', # attention : remplacez par votre nom d'utilisateur !!
        'PASSWORD': 'test123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

