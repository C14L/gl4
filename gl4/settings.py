"""
Django settings for gl4 project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""


# Import private settings.
from collections import OrderedDict
from os.path import dirname, abspath, exists, join
from gl4.settings_private import *

DEBUG = exists('/islocal.txt')
PRODUCTION = False

BASE_DIR = dirname(dirname(abspath(__file__)))

SITE_ID = 1
SITE_NAME = 'Graniteland.com'
SITE_DOMAIN = 'graniteland.com'  # default canonical domain

APPEND_SLASH = True
ROOT_URLCONF = 'gl4.urls'
WSGI_APPLICATION = 'gl4.wsgi.application'

ALLOWED_HOSTS = ['www.' + SITE_DOMAIN, 'localhost']
CANONICAL_BASE = 'http://{}'.format(ALLOWED_HOSTS[0])

EMAIL_HOST = 'localhost'
if DEBUG:
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
    'markdown_deux',
    'django_bleach',

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

    'gl4app',
    'companydb',
    'stonedb',
    'tradeshowdb',
    'mdpages',
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

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGE_SHORT = 'en'
LANGUAGES = [('en', 'english'), ('de', 'deutsch'), ]

TIME_ZONE = 'UTC'
USE_TZ = True
USE_I18N = True
USE_L10N = True
USE_ETAGS = True

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')

# Example: "/media/en/fotos_small/21392.jpg"
MEDIA_URL = '/media/{}/'.format(LANGUAGE_SHORT)
MEDIA_ROOT = '/home/chris/dev-data/gl4-media/' \
             'graniteland_media_{}/'.format(LANGUAGE_SHORT)

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

# --- crispy forms -------------------------------------------------------------

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG

# --- django-bleach ------------------------------------------------------------

BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a']

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
BLEACH_DEFAULT_WIDGET = 'wysiwyg.widgets.WysiwygWidget'

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
}

# --- my own settings ----------------------------------------------------------

STONES_PER_PAGE = 500  # Do not use pagination, better all on one page and then
                       # use JS on-demand loading of images when user scrolls.

WATERMARK_FONT_FILENAME = join(BASE_DIR, 'Verdana.ttf')
STONE_SEARCH_OPTS_FILE = join(BASE_DIR, 'api_static', 'stone-search-opts.json')
COMPANY_SEARCH_OPTS_FILE = join(BASE_DIR, 'api_static',
                                'company-search-opts.json')

COMPANY_CONTACT_FROM_EMAIL = 'contact@' + SITE_DOMAIN

FOOTER_BROWSE_STONES = {
    'color': (
        ('beige', 'Beige natural stone'),
        ('black', 'Black natural stone'),
        ('blue', 'Blue natural stone'),
        ('brown', 'Brown natural stone'),
        ('darkgrey', 'Dark grey natural stone'),
        ('green', 'Green natural stone'),
        ('grey', 'Grey natural stone'),
        ('lightgrey', 'Light grey natural stone'),
        ('pink', 'Pink natural stone'),
        ('red', 'Red natural stone'),
        ('white', 'White natural stone'),
        ('yellow', 'Yellow natural stone'),
    ),
    'country': (
        ('brazil', 'Granite and marble from Brazil'),
        ('china', 'Granite and marble from China'),
        ('germany', 'Granite and marble from Germany'),
        ('france', 'Granite and marble from France'),
        ('india', 'Granite and marble from India'),
        ('italy', 'Granite and marble from Italy'),
        ('spain', 'Granite and marble from Spain'),
    ),
    'type':(
        ('granite', 'Granite'),
        ('limestone', 'Limestone'),
        ('marble', 'Marble'),
        ('quartzite', 'Quartzite'),
        ('sandstone', 'Sandstone'),
        ('slate', 'Slate'),
        ('soapstone', 'Soapstone'),
        ('travertine', 'Travertine'),
    ),
}
