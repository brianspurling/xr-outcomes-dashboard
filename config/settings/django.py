import os
import environ
import dj_database_url

env = environ.Env()
environ.Env.read_env()  # reads the .env file

DEBUG = env('DEBUG', default=False)
SECRET_KEY = env('SECRET_KEY')

root = environ.Path(__file__) - 3
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEMPLATE_DEBUG = DEBUG

STATIC_ROOT = os.path.join(root, 'staticfiles')  # for deployment
STATICFILES_DIRS = (os.path.join(root, 'static'), )  # for local
STATIC_URL = '/static/'  # the URL that serves static files
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

ROOT_URLCONF = 'config.urls'

DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(root, 'templates/'),),
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ALLOWED_HOSTS = ['.herokuapp.com', 'localhost']
