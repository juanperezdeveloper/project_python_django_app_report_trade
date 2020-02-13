from datetime import datetime
from fabric.api import env, run
from fabric.utils import abort
from fabric.context_managers import settings

def prod():
    global DJANGO_ENV
    DJANGO_ENV = "prod"
    env.user = "deploy"
    env.hosts = ["96.126.110.177"] # linode119185

def deploy():

    global DJANGO_ENV
    if not DJANGO_ENV:
        abort("You must specify a Django environment to deploy.")

    now = datetime.now()
    dir_name = "%d-%02d-%02d-%02d-%02d-%02d" % (
        now.year,
        now.month,
        now.day,
        now.hour,
        now.minute,
        now.second
    )
    result = run('mkdir ~/apps/mlds/%s' % dir_name)
    if result.failed:
        abort("Couldn't create directory for enlistment.")

    # Pull Mercurial Repo on server
    result = run('hg pull -R ~/apps/mlds/hg_repo/django_mlds')
    if result.failed:
        abort("Couldn't pull Hg Repo")

    # Update Mercurial Repo on server
    result = run('hg update -R ~/apps/mlds/hg_repo/django_mlds')
    if result.failed:
        abort("Couldn't update Hg Repo")

    # Use hg archive to copy files from repo to dir_name
    result = run('hg archive -R ~/apps/mlds/hg_repo/django_mlds ~/apps/mlds/%s/django_mlds' % dir_name)
    if result.failed:
        abort("Couldn't copy files (hg archive)")

    with settings(warn_only=True):
        result = run('rm ~/apps/mlds/current')

    result = run('ln -s ~/apps/mlds/%s ~/apps/mlds/current' % dir_name)
    if result.failed:
        abort("Couldn't link to new enlistment.")

    result = run('rsync -r --exclude=.svn ~/apps/mlds/current/django_mlds/media/* ~/apps/mlds/media')
    if result.failed:
        abort("Couldn't copy media files.")

    result = run('cat ~/apps/mlds/current/django_mlds/settings_overrides/%s.py >> ~/apps/mlds/current/django_mlds/settings.py' % DJANGO_ENV)
    if result.failed:
        abort("Couldn't override settings")

    result = run('touch ~/apps/mlds/current/django_mlds/local_settings.py')
    if result.failed:
        abort("Couldn't create local settings file")

    result = run('mkdir -p ~/apps/mlds/nginx_links')
    if result.failed:
        abort("Couldn't make nginx links directory")

    result = run('ln -s ~/apps/mlds/media/ ~/apps/mlds/nginx_links/%s' % (dir_name))
    if result.failed:
        abort("Couldn't create new media link")

    # Append a line to settings.py that will add the dir_name to the Admin Media  prefix
    result = run("""echo ADMIN_MEDIA_PREFIX = MEDIA_URL + \\\"%s\\\" >>  ~/apps/mlds/current/django_mlds/settings.py""" % ("/" + dir_name + "/admin/"), shell=False)
    if result.failed:
        abort("Couldn't append setting to add dir_name to admin media URL")

    # Append a line to settings.py that will add the dir_name to the Media URL
    result = run("""echo MEDIA_URL = MEDIA_URL + \\\"%s\\\" >>  ~/apps/mlds/current/django_mlds/settings.py""" % ("/" + dir_name), shell=False)
    if result.failed:
        abort("Couldn't append setting to add dir_name to media URL")


    # stop nginx
    result = run("sudo /etc/init.d/nginx stop")
    if result.failed:
        abort("Couldn't stop nginx")

    # delete cache files
    result = run("sudo rm -rf /var/www/cache/*")
    if result.failed:
        abort("Couldn't delete cache")

    # re-start nginx
    result = run("sudo /etc/init.d/nginx start")
    if result.failed:
        abort("Couldn't start nginx")

    result = run('sudo /etc/init.d/apache2 restart')
    if result.failed:
        abort("Couldn't restart apache")
