
import re
import os

from os.path import dirname, abspath, exists, join

from gl4 import settings_private

# ==============================================================================

LANGUAGE_CODE = os.environ.get('GRANITELAND_LANGUAGE', None)

if not LANGUAGE_CODE:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured('Language must be explicitly set in '
                               'GRANITELAND_LANGUAGE environment variable.')

# ==============================================================================

BASE_DIR = dirname(dirname(abspath(__file__)))

DEVBOX = os.environ.get('ISDEV')
DEBUG = DEVBOX
PRODUCTION = not DEVBOX
SHOW_ADS = False
ENABLE_PROFILER = False
ENABLE_DEBUG_TOOLBAR = False
ENABLE_TIME_LOGGER = True
TIME_LOGGER_LOGFILE = '/tmp/gl4_time_logger.log'

LANGUAGE_SHORT = LANGUAGE_CODE[:2]

if LANGUAGE_CODE == 'de':
    LANGUAGES = [('de', 'Deutsch'), ]
else:
    LANGUAGES = [('en', 'English'), ]

SITE_ID = 1
APPEND_SLASH = True
WSGI_APPLICATION = 'gl4.wsgi.application'
ROOT_URLCONF = 'gl4.urls_{}'.format(LANGUAGE_CODE)

ADMINS = settings_private.ADMINS
MANAGERS = settings_private.MANAGERS
SECRET_KEY = settings_private.SECRET_KEY
ADSENSE_AD_CLIENT = settings_private.ADSENSE_AD_CLIENT

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        # 'NAME': 'graniteland',
        'USER': 'graniteland',
        'PASSWORD': settings_private.DATABASES_PASSWORD,
    },
}

if not PRODUCTION:
    DATABASES['default']['PASSWORD'] = 'pla'

if LANGUAGE_CODE == 'de':
    SITE_NAME = 'Graniteland.de'
    SITE_DOMAIN = 'graniteland.de'  # default canonical domain
    TEST_DOMAIN = 'glde.3dir.com'
    DATABASES['default']['NAME'] = 'gd'
else:
    SITE_NAME = 'Graniteland.com'
    SITE_DOMAIN = 'graniteland.com'  # default canonical domain
    TEST_DOMAIN = 'glen.3dir.com'
    DATABASES['default']['NAME'] = 'gc'

ALLOWED_HOSTS = ['www.' + SITE_DOMAIN, TEST_DOMAIN, 'localhost']
CANONICAL_BASE = 'https://{}'.format(ALLOWED_HOSTS[0])

# Email config
EMAIL_SUBJECT_PREFIX = 'El Ligue: '  # For system emails to ADMINS+MANAGERS.
SERVER_EMAIL = settings_private.SERVER_EMAIL
DEFAULT_FROM_EMAIL = settings_private.DEFAULT_FROM_EMAIL
EMAIL_HOST = settings_private.EMAIL_HOST
EMAIL_HOST_USER = settings_private.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings_private.EMAIL_HOST_PASSWORD
EMAIL_PORT = 25  # not 587
EMAIL_USE_TLS = True

if not PRODUCTION:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',  # required by allauth
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rosetta',
    'crispy_forms',
    'bootstrapform',
    'markdown_deux',
    'django_bleach',

    'gl4app',
    'companydb',
    'stonedb',
    'tradeshowdb',
    'mdpages',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'gl4app.middleware.FixSomeWordInflextionsMiddleware',
]

if ENABLE_DEBUG_TOOLBAR:
    print('ACTIVE: ENABLE_DEBUG_TOOLBAR')
    INSTALLED_APPS += ['debug_toolbar']
if ENABLE_PROFILER:
    print('ACTIVE: ENABLE_PROFILER')
    MIDDLEWARE.insert(0, 'gl4app.middleware.ProfilerMiddleware')
if ENABLE_TIME_LOGGER:
    print('ACTIVE: ENABLE_TIME_LOGGER')
    MIDDLEWARE.insert(0, 'gl4app.middleware.ExecTimeLoggerMiddleware')

TEMPLATE_CACHE_TIMEOUT = 60  # -> 1 min. // * 60 * 24 * 7  # 7 days
TEMPLATE_FOOTER_CACHE_TIMEOUT = 60 * 60 * 24 * 30  # -> 1 month

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
                'gl4app.context_processors.add_common_translations',
                'gl4app.context_processors.add_settings',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True
USE_ETAGS = True

# Only for development, served via Nginx in production.
STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')

# Only for development, served via Nginx in production.
# -- example: "/media/fotos_small/21392.jpg"

# Upload target is language dependent
MEDIA_URL = '/media/'
if PRODUCTION:
    d = '../../usercontent'
    MEDIA_ROOT = join(BASE_DIR, d, 'graniteland_media_{}'.format(LANGUAGE_SHORT))
else:
    d = '/space01/devdata/graniteland/usercontent'
    MEDIA_ROOT = join(d, 'graniteland_media_{}'.format(LANGUAGE_SHORT))

# --- django-autoslug settings -------------------------------------------------

AUTOSLUG_SLUGIFY_FUNCTION = 'django.utils.text.slugify'

# --- django-allauth settings --------------------------------------------------
# http://django-allauth.readthedocs.org/en/latest/configuration.html

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True  # user needs to provide and confirm email address
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Graniteland '
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True  # checked: no dupes in .com DB table
ACCOUNT_USERNAME_BLACKLIST = []
LOGIN_REDIRECT_URL = '/u/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_PASSWORD_MIN_LENGTH = 4

ACCOUNT_SIGNUP_FORM_CLASS = 'companydb.forms.CompanySignupForm'

# --- crispy forms -------------------------------------------------------------

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = PRODUCTION

# --- django-bleach ------------------------------------------------------------

BLEACH_ALLOWED_TAGS = ['h1', 'h2', 'h3', 'p', 'b', 'i', 'u', 'em', 'strong', 'a']

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style']

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES = ['font-family', 'font-weight', 'text-decoration', 'font-variant']

# Strip unknown tags if True, replace with HTML escaped characters if False
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = True

# Use the CKEditorWidget for bleached HTML fields
# BLEACH_DEFAULT_WIDGET = 'wysiwyg.widgets.WysiwygWidget'
# BLEACH_ALLOWED_PROTOCOLS = ['https']

# --- django-markdown-deux -----------------------------------------------------

MARKDOWN_DEUX_STYLES = {
    "default": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": "escape",
    },
    "trusted": {
        "extras": {
            "code-friendly": None,
        },
        "safe_mode": False,
    },
    'user': {
        "safe_mode": "escape",
        "link_patterns": [(
            re.compile(r'(granites?|marbles?|limestones?|sandstones?)', re.I),
            r"https://www.graniteland.com/stone/type/\1"
        ), ],
        "extras": {
            "code-friendly": None,
            "cuddled-lists": None,
            "footnotes": None,
            "header-ids": None,
        },
    }
}

# --- rosetta ------------------------------------------------------------------

# ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
# YANDEX_TRANSLATE_KEY
# AZURE_CLIENT_ID
# AZURE_CLIENT_SECRET
ROSETTA_EXCLUDED_APPLICATIONS = ('allauth', 'rosetta', )
# ROSETTA_EXCLUDED_PATHS = ('/**/site-packages/**/*', )

# --- my own settings ----------------------------------------------------------

# Mdpages pagination limit
MDPAGES_PER_PAGE = 50

STONEPIC_BASE = '/stonespics/'

# Do not use pagination, better all on one page and then use JS on-demand
# loading of images when user scrolls.
STONES_PER_PAGE = 500

WATERMARK_FONT_FILENAME = join(BASE_DIR, 'Verdana.ttf')

STONE_SEARCH_OPTS_FILE = join(
    BASE_DIR, 'api_static', 'stone-search-opts-{}.json'.format(LANGUAGE_CODE))
COMPANY_SEARCH_OPTS_FILE = join(
    BASE_DIR, 'api_static', 'company-search-opts-{}.json'.format(LANGUAGE_CODE))

COMPANY_CONTACT_FROM_EMAIL = 'contact@' + SITE_DOMAIN

# Companydb stock items are hidden after this many days
STOCK_EXPIRE_DAYS = 90

# Some parts of translated URL paths that may be different from the
# proper translation in the MO file.
if LANGUAGE_CODE == 'de':
    TR_COUNTRY = 'herkunftsland'
    TR_COLOR = 'farbe'
    TR_TEXTURE = 'textur'
    TR_CLASSIFICATION = 'steinart'
    TR_TYPE = 'steinart'

    TR_MDPAGES_HOME = 'zuhause'
    TR_MDPAGES_PROFESSIONAL = 'professionell'
    TR_MDPAGES_PRODUCTION = 'herstellung'
    TR_MDPAGES_MISC = 'vermischtes'
    TR_MDPAGES_HELP = 'hilfe'
else:
    TR_COUNTRY = 'country'
    TR_COLOR = 'color'
    TR_TEXTURE = 'texture'
    TR_CLASSIFICATION = 'classification'
    TR_TYPE = 'type'

    TR_MDPAGES_HOME = 'home'
    TR_MDPAGES_PROFESSIONAL = 'professional'
    TR_MDPAGES_PRODUCTION = 'production'
    TR_MDPAGES_MISC = 'misc'
    TR_MDPAGES_HELP = 'help'

DEBUG_TOOLBAR_PATCH_SETTINGS = DEBUG
DEBUG_TOOLBAR_CONFIG = {
    'INTERNAL_IPS': ['127.0.0.1', '::1'],
    'SHOW_TOOLBAR_CALLBACK': settings_private.show_toolbar_callback,
}
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    # 'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    # 'debug_toolbar.panels.redirects.RedirectsPanel',
]
