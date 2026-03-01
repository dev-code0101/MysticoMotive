import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Core Django settings ---

SECRET_KEY = os.getenv("SECRET_KEY", "insecure-secret-key-change-me")

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS", "localhost,127.0.0.1,mysticomotive.onrender.com"
).split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "corsheaders",
    # local apps
    "users",
    "stations",
    "trains",
    "bookings",
    "analytics",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "irctc_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "irctc_backend.wsgi.application"

# --- Database configuration (MySQL primary) ---

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "HOST": os.getenv("MYSQL_HOST", "localhost"),
#         "PORT": os.getenv("MYSQL_PORT", "3306"),
#         "NAME": os.getenv("MYSQL_DB", "irctc"),
#         "USER": os.getenv("MYSQL_USER", "irctc_user"),
#         "PASSWORD": os.getenv("MYSQL_PASSWORD", "irctc_password"),
#         "OPTIONS": {
#             "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            BASE_DIR, "db.sqlite3"
        ),  # BASE_DIR should be defined in your settings
    }
}

# --- Custom user model ---

AUTH_USER_MODEL = "users.User"

# --- Password validation ---

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# --- Internationalization ---

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

# --- Static files ---

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- REST framework & Simple JWT ---

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
}

ACCESS_TOKEN_LIFETIME_MINUTES = int(
    os.getenv("ACCESS_TOKEN_LIFETIME_MINUTES", "15")
)
REFRESH_TOKEN_LIFETIME_DAYS = int(os.getenv("REFRESH_TOKEN_LIFETIME_DAYS", "7"))

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME_DAYS),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --- CORS / security ---

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

CORS_ALLOW_ALL_ORIGINS = False if CORS_ALLOWED_ORIGINS else True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = (
    os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
)
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False").lower() == "true"
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "0"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "False").lower() == "true"
)
SECURE_HSTS_PRELOAD = (
    os.getenv("SECURE_HSTS_PRELOAD", "False").lower() == "true"
)

# --- MongoDB connection (for api_logs & analytics) ---

from pymongo import MongoClient  # noqa: E402

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/irctc")

mongo_client: MongoClient | None = None

if MONGO_URI:
    mongo_client = MongoClient(MONGO_URI)
