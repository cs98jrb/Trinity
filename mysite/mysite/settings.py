"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    BASE_DIR+"/mysite/templates/",
    BASE_DIR+"/polls/templates/",
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gjd#%4h1j+hjc4ha-(cj^-@rxde0i10yq7qw0)8jjtv2(38ivk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ADMINS = (('James', 'james@pjshire.me.uk'),)

EMAIL_HOST = 'mail.trinityrosewilliams.co.uk'
#EMAIL_HOST = 'mail.pjshire.me.uk'
EMAIL_HOST_USER = 'admin@trinitywilliams.co.uk'
EMAIL_HOST_PASSWORD = 'd/NMf-j,(Nc$bBP8T%>`'   

SERVER_EMAIL = 'admin@trinityrosewilliams.co.uk'

ALLOWED_HOSTS = ['mysite','127.0.0.1:8000']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
    'paypalrestsdk',
    'orders',
    'accounts',
    'system_emails',
    'mysite',
    'paypal',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {  
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': BASE_DIR+'/db.cnf',
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-GB'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR+'/static/'
STATICFILES_DIRS = (
    BASE_DIR+'/static/',
)

#

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR+'/media/'

# Paypal options
PAYPAL_MODE = 'sandbox' # sandbox or live
PAYPAL_CLIENT_ID =     'AY7PlxBVTw-rC9B2DkDXzJ8n-VIRLRI3ix1v743CPib8UtqjWMqKDsrEZDig'
PAYPAL_CLIENT_SECRET = 'ELL5tRAFy2c6_D3oNU4tSscVvOMlQdqC4koyqirnPFJJEHT5VW5llmI89_U5'
#PAYPAL_MODE = 'live' # sandbox or live
#PAYPAL_CLIENT_ID =     'ARlnjRDmelrLjCdt1ETnW84N_by2HGyHZcFgz5yWvtuVBzN-O1qmlYXmswB3'
#PAYPAL_CLIENT_SECRET = 'EH1MORAZQ9cDeTGXy2E4AmH63SOTe94xbeoPQkW6O9MFfWo5Hj-ErC74ZjHj'
PAYPAL_HOLD_BOOKING = 5

# change user model
AUTH_USER_MODEL = 'auth.User'
LOGIN_REDIRECT_URL = '/'

# vat registered
# False or the vat registration number
VAT_REGISTERED = False