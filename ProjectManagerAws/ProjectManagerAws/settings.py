"""
Django settings for ProjectManagerAws project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(w8=&=t83^_8yn0$9arfjv9o6pgffc85pi2qr0&yy%p@j^1&z$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['127.0.0.1','proj-mgr-aws.tsihnmkubk.us-west-2.elasticbeanstalk.com','0.0.0.0','dualstack.awseb-e-2-awsebloa-1cjtopb37kpm2-446718152.us-west-2.elb.amazonaws.com','projmgrtool.com',
#                  'django-env.eba-2wjaqpra.us-west-1.elasticbeanstalk.com']
ALLOWED_HOSTS = ['projmgrtool.com','django-env.eba-2wjaqpra.us-west-1.elasticbeanstalk.com','127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #adding contrib.sites for oauth
    'django.contrib.sites',
    'projectMgr',
    'crispy_forms',
    'bootstrapform',



    #rest framework
    'rest_framework',
    'rest_framework.authtoken',

    #rest_auth
    'rest_auth',
    'rest_auth.registration',

    #activity stream
    'actstream',


    #allauth specific
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # ... include the providers you want to enable:
    # 'allauth.socialaccount.providers.agave',
    # 'allauth.socialaccount.providers.amazon',
    # # 'allauth.socialaccount.providers.angellist',
    # # 'allauth.socialaccount.providers.asana',
    # 'allauth.socialaccount.providers.auth0',
    # 'allauth.socialaccount.providers.authentiq',
    # # 'allauth.socialaccount.providers.baidu',
    # # 'allauth.socialaccount.providers.basecamp',
    # # 'allauth.socialaccount.providers.bitbucket',
    # # 'allauth.socialaccount.providers.bitbucket_oauth2',
    # # 'allauth.socialaccount.providers.bitly',
    # # 'allauth.socialaccount.providers.cern',
    # # 'allauth.socialaccount.providers.coinbase',
    # # 'allauth.socialaccount.providers.dataporten',
    # # 'allauth.socialaccount.providers.daum',
    # # 'allauth.socialaccount.providers.digitalocean',
    # # 'allauth.socialaccount.providers.discord',
    # # 'allauth.socialaccount.providers.disqus',
    # # 'allauth.socialaccount.providers.douban',
    # # 'allauth.socialaccount.providers.draugiem',
    # 'allauth.socialaccount.providers.dropbox',
    # # 'allauth.socialaccount.providers.dwolla',
    # # 'allauth.socialaccount.providers.edmodo',
    # 'allauth.socialaccount.providers.edx',
    # # 'allauth.socialaccount.providers.eveonline',
    # 'allauth.socialaccount.providers.evernote',
    # 'allauth.socialaccount.providers.exist',
    # 'allauth.socialaccount.providers.facebook',
    # # 'allauth.socialaccount.providers.feedly',
    # # 'allauth.socialaccount.providers.fivehundredpx',
    # # 'allauth.socialaccount.providers.flickr',
    # # 'allauth.socialaccount.providers.foursquare',
    # # 'allauth.socialaccount.providers.fxa',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.gitlab',
    # 'allauth.socialaccount.providers.google',
    # # 'allauth.socialaccount.providers.hubic',
    # 'allauth.socialaccount.providers.instagram',
    # 'allauth.socialaccount.providers.jupyterhub',
    # # 'allauth.socialaccount.providers.kakao',
    # # 'allauth.socialaccount.providers.line',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.linkedin_oauth2',
    # # 'allauth.socialaccount.providers.mailru',
    # # 'allauth.socialaccount.providers.mailchimp',
    # 'allauth.socialaccount.providers.meetup',
    # 'allauth.socialaccount.providers.microsoft',
    # # 'allauth.socialaccount.providers.naver',
    # # 'allauth.socialaccount.providers.nextcloud',
    # # 'allauth.socialaccount.providers.odnoklassniki',
    # # 'allauth.socialaccount.providers.openid',
    # # 'allauth.socialaccount.providers.openstreetmap',
    # # 'allauth.socialaccount.providers.orcid',
    # 'allauth.socialaccount.providers.paypal',
    # 'allauth.socialaccount.providers.patreon',
    # 'allauth.socialaccount.providers.persona',
    # 'allauth.socialaccount.providers.pinterest',
    # 'allauth.socialaccount.providers.reddit',
    # 'allauth.socialaccount.providers.robinhood',
    # # 'allauth.socialaccount.providers.sharefile',
    # # 'allauth.socialaccount.providers.shopify',
    # # 'allauth.socialaccount.providers.slack',
    # 'allauth.socialaccount.providers.soundcloud',
    # 'allauth.socialaccount.providers.spotify',
    # 'allauth.socialaccount.providers.stackexchange',
    # 'allauth.socialaccount.providers.steam',
    # # 'allauth.socialaccount.providers.strava',
    # # 'allauth.socialaccount.providers.stripe',
    # # 'allauth.socialaccount.providers.trello',
    # # 'allauth.socialaccount.providers.tumblr',
    # # 'allauth.socialaccount.providers.twentythreeandme',
    # # 'allauth.socialaccount.providers.twitch',
    # 'allauth.socialaccount.providers.twitter',
    # # 'allauth.socialaccount.providers.untappd',
    # 'allauth.socialaccount.providers.vimeo',
    # 'allauth.socialaccount.providers.vimeo_oauth2',
    # # 'allauth.socialaccount.providers.vk',
    # # 'allauth.socialaccount.providers.weibo',
    # # 'allauth.socialaccount.providers.weixin',
    # # 'allauth.socialaccount.providers.windowslive',
    # # 'allauth.socialaccount.providers.xing',
    # # 'allauth.socialaccount.providers.yandex',
    # # 'allauth.socialaccount.providers.ynab',
]

#defining standard redirections
LOGIN_REDIRECT_URL = '/userhome/'

SITE_ID = 1
# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    # 'google': {
    #     # For each OAuth based provider, either add a ``SocialApp``
    #     # (``socialaccount`` app) containing the required client
    #     # credentials, or list them here:
    #     'APP': {
    #         'client_id': '123',
    #         'secret': '456',
    #         'key': ''
    #     }
    # }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProjectManagerAws.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(BASE_DIR,'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                #.request needed for oauth
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProjectManagerAws.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:

    DATABASES = {
        # 'default': {
        #     # 'ENGINE': 'django.db.backends.postgresql',
        #     'ENGINE':'django.db.backends.postgresql_psycopg2',
        #     'NAME':'mydb1',
        #     # 'HOST':database-1.cdo5huoba6lc.us-west-2.rds.amazonaws.com,
        #     # 'NAME':postgres,
        #     # 'PASSWORD':DbkzngcbZ1z4w66jgDaN,
        #     # 'NAME': os.path.join(BASE_DIR, 'postdb'),
        #     'USER': 'ganesh',
        #     'PASSWORD': 'ganesh',
        #     'HOST': 'localhost',
        #
        #     'HOST':'0.0.0.0',
        #     'PORT': '5432',
        # } ,

        # 'default': {
        #     # 'ENGINE': 'django.db.backends.postgresql',
        #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #     'NAME': 'database-1',
        #     # 'HOST':database-1.cdo5huoba6lc.us-west-2.rds.amazonaws.com,
        #     # 'NAME':postgres,
        #     # 'PASSWORD':DbkzngcbZ1z4w66jgDaN,
        #     # 'NAME': os.path.join(BASE_DIR, 'postdb'),
        #     'USER': 'postgres',
        #     'PASSWORD': 'GLOgpT9EBJ2EZD7Ja35c',
        #     'HOST': 'database-1.cbhzbc7blcip.us-west-1.rds.amazonaws.com',
        #     'PORT': '5432',
        # }
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    # 'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]

#allauth settings
# ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_CONFIRM_EMAIL_ON_GET =True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE =False

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
# TIME_ZONE = 'america/mazatlan'
USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = 'static'

AUTH_USER_MODEL = 'projectMgr.User'

CRISPY_TEMPLATE_PACK = 'bootstrap4'


#rest framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework.authentication.BasicAuthentication','rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',],

    'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated',],
}

#notification
# ACTSTREAM_SETTINGS = {
#     # 'MANAGER': 'Project projec.managers.MyActionManager',
#     'MANAGER':'Proje',
#     'FETCH_RELATIONS': True,
#     'USE_PREFETCH': True,
#     'USE_JSONFIELD': True,
#     'GFK_FETCH_DEPTH': 1,
# }

#HTTPS stuff
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True