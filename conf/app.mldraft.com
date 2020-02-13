WSGIScriptAlias / /home/deploy/apps/mlds/current/django_mlds/django.wsgi
<Directory /home/deploy/apps/mlds/current/django_mlds>
Order deny,allow
Allow from all
SetEnv DJANGO_ENV prod
</Directory>
