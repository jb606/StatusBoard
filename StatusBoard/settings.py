from pathlib import Path
import os
import environ
from django.core.exceptions import ImproperlyConfigured
import dj_database_url
from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(SB_DEBUG=(bool, False),
                  SB_ENABLE_OIDC=(bool, False))

try:
    environ.Env.read_env(str(BASE_DIR / '.env'))
except:
    raise ImproperlyConfigured(f"Missing required env file {BASE_DIR}/.env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

DEBUG = env('SB_DEBUG')
SECRET_KEY = env('SB_SECRET_KEY', default=get_random_secret_key())
ALLOWED_HOSTS = env.list("SB_ALLOWED_HOSTS", default=[])
DATA_DIR = env('SB_DATA_DIR', default=BASE_DIR)


# Application definition

INSTALLED_APPS = [
    "UserManager",
    "menubar",
    "django_htmx",
    "django_bootstrap5",
    "django_bootstrap_icons",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.openid_connect",
    "django_tables2",
    "django_filters",
    "crispy_forms",
    "crispy_bootstrap5",
    "StatusApp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "StatusBoard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR /'templates'),
                 os.path.join(BASE_DIR /'templates/allauth')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "menubar.context_processors.menu_items",
            ],
        },
    },
]

WSGI_APPLICATION = "StatusBoard.wsgi.application"


DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{DATA_DIR / 'db.sqlite3'}",
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    "static/",
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "StatusBoard/staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CRISPY_TEMPLATE_PACK = "bootstrap5"
AUTH_USER_MODEL = "UserManager.Person"

if env('SB_ENABLE_OIDC'):
    SITE_ID = 1
    LOGIN_REDIRECT_URL = "/"
    ACCOUNT_EMAIL_VERIFICATION = "none"
    SOCIALACCOUNT_AUTO_SIGNUP = True
    SOCIALACCOUNT_LOGIN_ON_GET = True
    SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
    SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
    SOCIALACCOUNT_ADAPTER = 'UserManager.adapters.MySocialAccountAdapter'
    SOCIALACCOUNT_PROVIDERS = {
        "openid_connect": {
            "APPS": [
                {
                    "provider_id": "sso_1",
                    "name": env('SB_OIDC_NAME'),
                    "client_id": env('SB_OIDC_CLIENT_ID'),
                    "secret": env('SB_OIDC_CLIENT_SECRET'),
                    "settings": {
                        "server_url": env('SB_OIDC_PROVIDER_URL'),
                        "fetch_userinfo": True,
                    }

                }
            ]
        }
    }
    OIDC_SITE_ADMIN_ROLE = env("SB_OIDC_SITE_ADMIN_ROLE", default="site-admins")
    OIDC_STAFF_ROLE = env("SB_OIDC_STAFF_ROLE", default="staff")
    OIDC_GROUPADM_ROLE = env("SB_GROUPADM_ROLE", default="status-admins")