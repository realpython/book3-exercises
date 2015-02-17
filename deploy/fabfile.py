from fabric.api import *

env.hosts = ['128.199.202.178']
env.user = 'root'


def ci():
    integrate()
    update_app()
    update_config()


def update_app():
    with cd("/opt/mec_env/mec_app"):
        run("git pull")
    with cd("/opt/mec_env/mec_app/django_ecommerce"):
        with prefix("source /opt/mec_env/bin/activate"):
            run("pip install -r ../requirements.txt")
            run("./manage.py migrate --noinput")
            run("./manage.py collectstatic --noinput")

def update_config():
    with cd("/opt/mec_env/mec_app/deploy"):
        run("cp settings_prod.py ../django_ecommerce/django_ecommerce/")
        run("cp supervisor/mec.conf /etc/supervisor/conf.d/")
        run("cp nginx/sites-avaliable/mec /etc/nginx/sites-available/")
        run("/etc/init.d/supervisor restart")
        run("/etc/init.d/nginx restart")

def integrate():
    with lcd("../django_ecommerce/"):
        local("pwd")
        local("./manage.py test ../tests/unit")

        with settings(warn_only=True):
            local("git add -p && git commit")

        local("git pull")
        #local("./manage.py test ../tests")
        local("git push")

