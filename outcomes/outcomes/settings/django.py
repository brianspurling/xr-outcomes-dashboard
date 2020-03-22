import os
import environ
env = environ.Env()
environ.Env.read_env()  # reads the .env file

DEBUG = env('DEBUG', default=False)

SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': env.db(),
}

root = environ.Path(__file__) - 3
env = environ.Env()

TEMPLATE_DEBUG = DEBUG

STATIC_URL = os.path.join(root, env.str('STATIC_URL', default='static/'))
STATIC_ROOT = env.str('STATIC_ROOT', default='/static/')

STATICFILES_DIRS = [os.path.join(root, 'static')]

ROOT_URLCONF = 'outcomes.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'outcomes.apps.dashboard',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (root.path('outcomes/templates'),),
        'APP_DIRS': False,
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
]
