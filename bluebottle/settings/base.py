# coding=utf-8
# Django settings for bluebottle project.

import os
# Import global settings for overriding without throwing away defaults
from django.conf import global_settings
from django.utils.translation import ugettext as _


# Set PROJECT_ROOT to the dir of the current file
# Find the project's containing directory and normalize it to refer to
# the project's root more easily
PROJECT_ROOT = os.path.dirname(os.path.normpath(os.path.join(__file__, '..', '..')))

# DJANGO_PROJECT: the short project name
# (defaults to the basename of PROJECT_ROOT)
DJANGO_PROJECT = os.path.basename(PROJECT_ROOT.rstrip('/'))

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    ('Ben Konrath', 'ben@1procentclub.nl'),
    ('Loek van Gent', 'loek@1procentclub.nl'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.onepercentclub.com', '.1procentclub.nl']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'


# Available user interface translations
# Ref: https://docs.djangoproject.com/en/1.4/ref/settings/#languages
#
# Default language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

# This is defined here as a do-nothing function because we can't import
# django.utils.translation -- that module depends on the settings.
gettext_noop = lambda s: s

LANGUAGES = (
    ('nl', gettext_noop('Dutch')),
    ('en', gettext_noop('English'))
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# First one is for apps the second for the main templates
LOCALE_PATHS = ('../locale', 'locale')

# If you set this to False, Django will not use timezone-aware datetimes.
# pytz is in requirements.txt because it's "highly recommended" when using
# timezone support.
# https://docs.djangoproject.com/en/1.4/topics/i18n/timezones/
USE_TZ = True


# Static Files and Media
# ======================
#
# For staticfiles and media, the following convention is used:
#
# * '/static/media/': Application media default path
# * '/static/global/': Global static media
# * '/static/assets/<app_name>/': Static assets after running `collectstatic`
#
# The respective URL's (available only when `DEBUG=True`) are in `urls.py`.
#
# More information:
# https://docs.djangoproject.com/en/1.4/ref/contrib/staticfiles/

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static', 'media')

# Absolute filesystem path to the directory that will hold PRIVATE user-uploaded files.
PRIVATE_MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'private', 'media')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/static/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static', 'assets')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/assets/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # You can also name this tuple like: ('css', '/path/to/css')
    (os.path.join(PROJECT_ROOT, 'static', 'global')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
]

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
]

# These are basically the default values from the Django configuration, written
# as a list for easy manipulation. This way one can:
#
# 1. Easily add, remove or replace elements in the list, ie. overriding.
# 2. Know what the defaults are, if you want to change them right here. This
#   way you won't have to look them up every time you want to change.
#
# Note: The first three middleware classes need to be in this order: Session, Locale, Common
# http://stackoverflow.com/questions/8092695/404-on-requests-without-trailing-slash-to-i18n-urls
MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # https://docs.djangoproject.com/en/1.4/ref/clickjacking/
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',

    'apps.redirects.middleware.RedirectFallbackMiddleware',
    'apps.crawlable.middleware.HashbangMiddleware',
]

# Browsers will block our pages from loading in an iframe no matter which site
# made the request. This setting can be overridden on a per response or a per
# view basis with the @xframe decorators.
X_FRAME_OPTIONS = 'DENY'


TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    # Makes the 'request' variable (the current HttpRequest) available in templates.
    'django.core.context_processors.request',
    'django.core.context_processors.i18n'
)

ROOT_URLCONF = 'bluebottle.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bluebottle.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates')
)

INSTALLED_APPS = (
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'django_extensions',
    'django_extensions.tests',
    'debug_toolbar',
    'raven.contrib.django',
    'djcelery',
    'south',
    'django_nose',
    'compressor',
    'sorl.thumbnail',
    'taggit',
    'taggit_autocomplete_modified',
    'micawber.contrib.mcdjango', # Embedding videos
    'templatetag_handlebars',
    'rest_framework',
    'polymorphic',
    'registration',
    'filetransfers',

    # CMS page contents
    'fluent_contents',
    'fluent_contents.plugins.text',
    'fluent_contents.plugins.oembeditem',
    'fluent_contents.plugins.rawhtml',
    'django_wysiwyg',
    'tinymce',
    'social_auth',
    'statici18n',

    # Cowry Payments
    'apps.cowry',
    'apps.cowry_docdata',

    # bluebottle apps
    'apps.blogs',
    'apps.bluebottle_dashboard',
    'apps.bluebottle_utils',
    'apps.contentplugins',
    'apps.accounts',
    'apps.love',
    'apps.organizations',
    'apps.projects',
    'apps.fund',
    'apps.geo',
    'apps.hbtemplates',
    'apps.wallposts',
    'apps.payouts',
    'apps.sepa',

    'apps.tasks',
    'apps.banners',
    'apps.quotes',
    'apps.statistics',
    'apps.pages',
    'apps.homepage',
    'apps.redirects',
    'apps.partners',

    # Custom dashboard
    'fluent_dashboard',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# log errors & warnings
import logging
logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] %(levelname)-8s %(message)s', datefmt="%d/%b/%Y %H:%M:%S")


# Django Celery - asynchronous task server
import djcelery
djcelery.setup_loader()


AUTHENTICATION_BACKENDS = (
    # 'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    # 'social_auth.backends.google.GoogleOAuthBackend',
    # 'social_auth.backends.google.GoogleOAuth2Backend',
    # 'social_auth.backends.google.GoogleBackend',
    # 'social_auth.backends.yahoo.YahooBackend',
    # 'social_auth.backends.browserid.BrowserIDBackend',
    # 'social_auth.backends.contrib.linkedin.LinkedinBackend',
    # 'social_auth.backends.contrib.disqus.DisqusBackend',
    # 'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    # 'social_auth.backends.contrib.orkut.OrkutBackend',
    # 'social_auth.backends.contrib.foursquare.FoursquareBackend',
    # 'social_auth.backends.contrib.github.GithubBackend',
    # 'social_auth.backends.contrib.vk.VKOAuth2Backend',
    # 'social_auth.backends.contrib.live.LiveBackend',
    # 'social_auth.backends.contrib.skyrock.SkyrockBackend',
    # 'social_auth.backends.contrib.yahoo.YahooOAuthBackend',
    # 'social_auth.backends.contrib.readability.ReadabilityBackend',
    # 'social_auth.backends.contrib.fedora.FedoraBackend',
    # 'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# We're using nose because it limits the tests to our apps (i.e. no Django and
# 3rd party app tests). We need this because tests in contrib.auth.user are
# failing in Django 1.4.1. Here's the ticket for the failing test:
# https://code.djangoproject.com/ticket/17966
# The new test runner in Django 1.5 will be more flexible:
#https://code.djangoproject.com/ticket/17365
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--detailed-errors',
    '--nologcapture',
]


SOUTH_TESTS_MIGRATE = False  # Make south shut up during tests


# django-compressor http://pypi.python.org/pypi/django_compressor
# Compressor is enabled whenever DEBUG is False.
STATICFILES_FINDERS += [
    # django-compressor staticfiles
    'compressor.finders.CompressorFinder',
]

# TODO Enable compass here.
COMPRESS_OUTPUT_DIR = 'compressed'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    #'compressor.filters.datauri.DataUriFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]

# Automagic CSS precompilation
#COMPRESS_PRECOMPILERS = (
#    ('text/coffeescript', 'coffee --compile --stdio'),
#    ('text/less', 'lessc {infile} {outfile}'),
#    ('text/x-sass', 'sass {infile} {outfile}'),
#    ('text/x-scss', 'sass --scss {infile} {outfile}'),
#)

# The default URL to send users to after login. This will be used when the
# 'next' URL parameter hasn't been set.
LOGIN_REDIRECT_URL = '/'

# Custom User model
AUTH_USER_MODEL = 'accounts.BlueBottleUser'

# Blog/news content configuration
FLUENT_CONTENTS_CACHE_OUTPUT = True
FLUENT_TEXT_CLEAN_HTML = True
FLUENT_TEXT_SANITIZE_HTML = True
DJANGO_WYSIWYG_FLAVOR = 'tinymce_advanced'

# Custom dashboard configuration
ADMIN_TOOLS_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentAppIndexDashboard'
ADMIN_TOOLS_MENU = 'fluent_dashboard.menu.FluentMenu'

# Further customize the dashboard
FLUENT_DASHBOARD_DEFAULT_MODULE = 'admin_tools.dashboard.modules.AppList'
FLUENT_DASHBOARD_APP_GROUPS = (
    (_('Site content'), {
        'models': [
            'apps.pages.*',
            'apps.blogs.*',
            'apps.media.*',
            'apps.banners.*',
            'apps.quotes.*',
            'apps.statistics.*',
        ],
        'module': 'fluent_dashboard.modules.AppIconList',
        'collapsible': False,
    }),
    (_('Projects'), {
        'models': (
            'apps.projects.models.Message',
            'apps.projects.models.Project',
            'apps.projects.models.ProjectPitch',
            'apps.projects.models.ProjectPlan',
            'apps.projects.models.Testimonial',
            'apps.organizations.*',
            'apps.donations.*',
        ),
        'module': 'fluent_dashboard.modules.AppIconList',
        'collapsible': False,
    }),
    (_('Funding'), {
        'models': (
            'apps.fund.*',
            'apps.vouchers.*',
            'apps.payouts.models.BankMutation',
            'apps.payouts.models.Payout',
        ),
        'module': 'fluent_dashboard.modules.AppIconList',
        'collapsible': False,
    }),
    (_('Tasks'), {
        'models': (
            'apps.tasks.*',
        ),
        'module': 'fluent_dashboard.modules.AppIconList',
        'collapsible': False,
    }),
    (_('Administration'), {
        'models': (
            'django.contrib.auth.*',
            'django.contrib.sites.*',
            'apps.accounts.*',
        ),
        'module': 'fluent_dashboard.modules.AppIconList',
        'collapsible': False,
    }),
    # The '*' selector acts like a fallback for all other apps. This section mainly displays models
    # with tabular data that is rarely touched. The important models have an icon.
    (_('Applications'), {
        'models': ('*',),
        'module': FLUENT_DASHBOARD_DEFAULT_MODULE,
        'collapsible': False,
    }),
)

# Icon filenames can either be relative to the theme directory (if no path separators are used),
# or be a relative to the STATIC_URL (if path separators are used in the icon name)
# The dictionary key is appname/modelname, identical to the slugs used in the admin page URLs
# django-fluent-dashboard ships with a set of commonly useful icons. To get the whole Oxygen set,
# download http://download.kde.org/stable/4.9.0/src/oxygen-icons-4.9.0.tar.xz It's LGPL3 licensed.
FLUENT_DASHBOARD_APP_ICONS = {
    'accounts/userprofile': 'user-identity.png',
    'blogs/blogpostproxy': 'view-pim-journal.png',
    'blogs/newspostproxy': 'view-calendar-list.png',
    'media/album': 'folder-image.png',
    'donations/donation': 'help-donate.png',
    'organizations/organization': 'x-office-address-book.png',
    'organizations/organizationmember': 'x-office-contact.png',
    'projects/message': 'accessories-text-editor.png',  # 'view-conversation-balloon.png',
    'projects/testimonial': 'help-feedback.png',
    'projects/project': 'view-time-schedule.png',
}

# Required for handlebars_template to work properly
USE_EMBER_STYLE_ATTRS = True

# Sorl Thumbnail settings
# http://sorl-thumbnail.readthedocs.org/en/latest/reference/settings.html
THUMBNAIL_QUALITY = 85
# TODO: Configure Sorl with Redis.

REST_FRAMEWORK = {
    'FILTER_BACKEND': 'rest_framework.filters.DjangoFilterBackend',
    # Don't do basic authentication.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}

COWRY_RETURN_URL_BASE = 'http://127.0.0.1:8000'

COWRY_PAYMENT_METHODS = {
    'dd-webmenu': {
        'profile': 'webmenu',
        'name': 'Web Menu',
        'supports_recurring': False,
        'supports_single': True,
    },

    'dd-direct-debit': {
        'id': 'DIRECT_DEBIT',
        'profile': 'directdebit',
        'name': 'Direct Debit',
        'max_amount': 10000,  # €100
        'restricted_countries': ('NL',),
        'supports_recurring': True,
        'supports_single': False,
    },
}

# The rate that is payed out to projects
PROJECT_PAYOUT_RATE = 0.95

# Settings for organization bank account. Please set this in secrets.py
# SEPA = {
#     'iban': '',
#     'bic': '',
#     'name': '',
#     'id': ''
# }

# Salesforce app settings
SALESFORCE_QUERY_TIMEOUT = 3
DATABASE_ROUTERS = [
    "salesforce.router.ModelRouter"
]

# E-mail settings
DEFAULT_FROM_EMAIL = '<website@onepercentclub.com> 1%Club'


# Django-registration settings
ACCOUNT_ACTIVATION_DAYS = 4
HTML_ACTIVATION_EMAIL = True  # Note this setting is from our forked version.

# Functional testing
# Selenium and Splinter settings
SELENIUM_TESTS = False
SELENIUM_WEBDRIVER = 'phantomjs'  # Can be any of chrome, firefox, phantomjs

FIXTURE_DIRS = [
    os.path.join(DJANGO_PROJECT, 'fixtures')
]

# PhantomJS for flat page generation.
# NOTE: This has nothing to do with testing against phantomjs.
CRAWLABLE_PHANTOMJS_DEDICATED_MODE = True
# If dedicated mode is enabled, configure the port:
CRAWLABLE_PHANTOMJS_DEDICATED_PORT = 8910
# If dedicated mode is disabled, you can specify arguments to start phantomjs.
CRAWLABLE_PHANTOMJS_ARGS = []

# Send email to console by default
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICI18N_ROOT = os.path.join(PROJECT_ROOT, 'static', 'global')
