INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

EXTERNAL_INSTALLED_APPS = [

    #  for authentications
    'allauth',
    'allauth.account',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework',
    #  if using token authentication
    'rest_framework.authtoken',
    #  using only jwt
    'rest_framework_simplejwt',

    # for running tasks
    'django_celery_beat',
    #  for logging and sending mail
    #  it enable us to view failed and sent mails
    # Corsheaders
    "corsheaders",
]

LOCAL_INSTALLED_APPS = [
    'users',
    'companies',
    'feedbacks',
    'leads',
    'schedules',
    'high_value_contents',
    'events',
    'careers',
    'communications',
    'email_logs',
    'contacts',
]
INSTALLED_APPS += EXTERNAL_INSTALLED_APPS
INSTALLED_APPS += LOCAL_INSTALLED_APPS
