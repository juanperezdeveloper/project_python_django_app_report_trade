# Add Production Settings here

DJANGO_ENV = "prod"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mlds',                      # Or path to database file if using sqlite3.
        'USER': 'mldraft',                      # Not used with sqlite3.
        'PASSWORD': 'yriy0WR9LAgxXV',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TEMPLATE_DIRS = (
    "/home/deploy/apps/mlds/current/django_mlds/acefs/templates"
)

# End with a Blank Line !

