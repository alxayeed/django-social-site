import os
from . import cred
from django.urls import reverse_lazy

# dynamically adds get_absolute_url for all objects of specified model(auth.user)
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('account:user_detail',
                                        args=[u.username])
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zipsuwk43i3n#09n$k%x-m1#1o36)6t@vjj17(pa9r%-crnd_0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['alapp.com', 'localhost', '127.0.0.1', ]


# Application definition

INSTALLED_APPS = [
    # this app must come before admin app to use this app's template first
    'account.apps.AccountConfig',
    'images.apps.ImagesConfig',
    'actions.apps.ActionsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'django_extensions',
    'easy_thumbnails',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# DJango static file finder will first look this subdirectory of every app
STATIC_URL = '/static/'
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "account/static"),
# )

# DEFAULT URL TO USE BY AUTH VIEWS
# @login_required will be redirected here with a next value in request
LOGIN_URL = 'account:login'
LOGOUT_URL = 'account:logout'
LOGIN_REDIRECT_URL = 'account:dashboard'

# Using Django Email Backend to write email to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# configuration for MEDIA files
MEDIA_URL = '/media/'
# media files will be stored here
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# AUTHENTICATION BACKEND
# use this command to run using ssl -  python manage.py runserver_plus --cert-file cert.crt
AUTHENTICATION_BACKENDS = [
    # Default, first check for username X password
    'django.contrib.auth.backends.ModelBackend',
    # if not found, check for the custom one - email X Password
    'account.authentication.EmailAuthBackend',
    # authentication for Facbook OAuth
    'social_core.backends.facebook.FacebookOAuth2',
    # Authentication backend for Google
    'social_core.backends.google.GoogleOAuth2',
]

# Facebook Auth
SOCIAL_AUTH_FACEBOOK_KEY = cred.APP_ID  # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = cred.APP_SECRET  # Facebook App Secret
# extra permissions this app will ask for to facebook user
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

# Google_Auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = cred.CLIENT_ID  # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = cred.CLIENT_SECRET  # Google Consumer Secret

# REDIS CONFIG
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
