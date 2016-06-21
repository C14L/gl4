"""
Django settings for gl4 project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import re
from os import environ
from os.path import dirname, abspath, exists, join

# Import private settings.
from gl4.settings_private import *

# ==============================================================================

LANGUAGE_CODE = environ.get('GRANITELAND_LANGUAGE', 'en')

# ==============================================================================

DEBUG = exists('/islocal.txt')
PRODUCTION = not DEBUG
SHOW_ADS = False

BASE_DIR = dirname(dirname(abspath(__file__)))

LANGUAGE_SHORT = LANGUAGE_CODE[:2]

if LANGUAGE_CODE == 'de':
    LANGUAGES = [('de', 'Deutsch'), ]
else:
    LANGUAGES = [('en', 'English'), ]

SITE_ID = 1
APPEND_SLASH = True
WSGI_APPLICATION = 'gl4.wsgi.application'
ROOT_URLCONF = 'gl4.urls_{}'.format(LANGUAGE_CODE)

if LANGUAGE_CODE == 'de':
    SITE_NAME = 'Graniteland.de'
    SITE_DOMAIN = 'graniteland.de'  # default canonical domain
    TEST_DOMAIN = 'glde.cn8.eu'
    if PRODUCTION:
        DATABASES['default']['NAME'] = 'gd'
    else:
        DATABASES['default']['NAME'] = 'gd_dev'
else:
    SITE_NAME = 'Graniteland.com'
    SITE_DOMAIN = 'graniteland.com'  # default canonical domain
    TEST_DOMAIN = 'glen.cn8.eu'
    if PRODUCTION:
        DATABASES['default']['NAME'] = 'gc'
    else:
        DATABASES['default']['NAME'] = 'gc_dev'

ALLOWED_HOSTS = ['www.' + SITE_DOMAIN, TEST_DOMAIN, 'localhost']
CANONICAL_BASE = 'http://{}'.format(ALLOWED_HOSTS[0])

if not PRODUCTION:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Application definition

INSTALLED_APPS = (
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

    # comes last so the templates can be overridden
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers.amazon',
    # 'allauth.socialaccount.providers.angellist',
    # 'allauth.socialaccount.providers.bitbucket',
    # 'allauth.socialaccount.providers.bitly',
    # 'allauth.socialaccount.providers.coinbase',
    # 'allauth.socialaccount.providers.dropbox',
    # 'allauth.socialaccount.providers.dropbox_oauth2',
    # 'allauth.socialaccount.providers.edmodo',
    # 'allauth.socialaccount.providers.evernote',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.flickr',
    # 'allauth.socialaccount.providers.feedly',
    # 'allauth.socialaccount.providers.fxa',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.hubic',
    # 'allauth.socialaccount.providers.instagram',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.linkedin_oauth2',
    # 'allauth.socialaccount.providers.odnoklassniki',
    # 'allauth.socialaccount.providers.openid',
    # 'allauth.socialaccount.providers.persona',
    # 'allauth.socialaccount.providers.soundcloud',
    # 'allauth.socialaccount.providers.spotify',
    # 'allauth.socialaccount.providers.stackexchange',
    # 'allauth.socialaccount.providers.stripe',
    # 'allauth.socialaccount.providers.tumblr',
    # 'allauth.socialaccount.providers.twitch',
    # 'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.vimeo',
    # 'allauth.socialaccount.providers.vk',
    # 'allauth.socialaccount.providers.weibo',
    # 'allauth.socialaccount.providers.xing',

    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'gl4app.middleware.FixSomeWordInflextionsMiddleware'
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # 'loaders': [
            #    ('django.template.loaders.cached.Loader', [
            #        'django.template.loaders.filesystem.Loader',
            #        'django.template.loaders.app_directories.Loader',
            #    ]),
            # ],
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
    MEDIA_ROOT = join(BASE_DIR, '../../usercontent',
                      'graniteland_media_{}'.format(LANGUAGE_SHORT))
else:
    MEDIA_ROOT = join('/home/chris/dev-data/gl4-media',
                      'graniteland_media_{}'.format(LANGUAGE_SHORT))

# --- django-autoslug settings -------------------------------------------------

AUTOSLUG_SLUGIFY_FUNCTION = 'django.utils.text.slugify'

# --- django-allauth settings --------------------------------------------------
# http://django-allauth.readthedocs.org/en/latest/configuration.html

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True  # user needs to provide and confirm email address
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'Graniteland '
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True  # checked: no dupes in .com DB table
ACCOUNT_USERNAME_BLACKLIST = []
ACCOUNT_PASSWORD_MIN_LENGTH = 4  # def: 6
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# --- crispy forms -------------------------------------------------------------

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = PRODUCTION

# --- django-bleach ------------------------------------------------------------

BLEACH_ALLOWED_TAGS = ['h1', 'h2', 'h3', 'p', 'b', 'i', 'u', 'em', 'strong', 'a']

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style']

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES = ['font-family', 'font-weight', 'text-decoration',
                         'font-variant']

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
