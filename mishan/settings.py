# Django settings for mishan project.
import os

MODE = os.getenv ( "MODE", "PRODUCTION" )

if MODE == "DEVELOPMENT":
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

FORCE_SCRIPT_NAME = ""

if MODE == "PRODUCTION":
    PATH_ROOT = "/home/ubuntu/install/mishan"
else:
    PATH_ROOT = "/home/ubuntu/install/mishan"
    #PATH_ROOT = os.getcwd()

ADMINS = (
    ('Nimisha Srivastava', 'nsrivastava@mishanenergy.com'),
)

MANAGERS = ADMINS
LINE_MANAGERS = [ "nimisha.sri1@gmail.com", "anjanikumar@mishanenergy.com", "nsrivastava@mishanenergy.com", "swapnil@mishanenergy.com"]

if MODE == "PRODUCTION":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mishan',                      # Or path to database file if using sqlite3.
            'USER': 'ubuntu',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            #'USER': 'admin',                      # Not used with sqlite3.
            #'PASSWORD': 'S2KHl2pekg19',                  # Not used with sqlite3.
            #'HOST': '127.7.153.1',                      # Set to empty string for localhost. Not used with sqlite3.
            #'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mishan',                      # Or path to database file if using sqlite3.
            'USER': 'ubuntu',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = "" #os.path.join ( os.getcwd(), "static" )

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
#ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join ( os.getcwd(), "static" ),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'y^)jj(&u&)3!6ey!v9yr^ilm@krc9blzq^9n#(mn_%mz_emh@8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'mishan.energy.generalmiddleware.GeneralMiddleware',
)

ROOT_URLCONF = 'mishan.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join ( PATH_ROOT, "mishan", "templates" ),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mishan.energy',
    # Uncomment the next line to enable the admin:
    #'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

MENU = (
    ("", "HOME"),
    ("aboutus", "About Us"),
    ("services", "Services"),
    ("newsnevents", "News & Events"),
    #("blog", "Blog"),
    ("contactus", "Contact Us"),
)

SERVICES = (
    ("development", "Website Development"),
    ("designing", "Designing"),
    ("fad", "Facebook Application Development"),
    ("smm", "Social Media Marketing"),
    ("seo", "Search Engine Optimization"),
)

SERVER_EMAIL = "support@mishanenergy.com"

EMAIL_HOST = "email-smtp.us-east-1.amazonaws.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "AKIAI5YJ46G24MRR2RYA"
EMAIL_HOST_PASSWORD = "AlWw9h9rbL6qQJB+lhbrXaZovBaiIwh2GidUaLfyLjV2"
EMAIL_USE_TLS = True

LOGIN_URL = "/auth/login"
EMAIL_REGEX = "[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}"

MARK_DOWN = os.path.join ( PATH_ROOT, "mishan", "markdown", MODE.lower() )

AWS_ACCESS_KEY_ID = file ("/home/ubuntu/.s3.key").read ().split (":")[0].strip()
AWS_SECRET_ACCESS_KEY = file ("/home/ubuntu/.s3.key").read ().split (":")[1].strip()
S3_KEY = AWS_ACCESS_KEY_ID
S3_SECRET = AWS_SECRET_ACCESS_KEY

REDIRECTION_RULES = [ ('mishanenergy.com'), 'www.mishanenergy.com' ]

#WEBFACTION_USER = 'tunesdiary'
#WEBFACTION_PASSWORD = 'webfactioni586'

MASTER_PASSWORD = "0bf6dbeb97b5572136feea58455e5733" #ss


