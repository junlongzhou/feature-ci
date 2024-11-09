#!/bin/sh

# Make sure we're not confused by old, incompletely-shutdown httpd
# context after restarting the container.  httpd won't start correctly
# if it thinks it is already running.

. /tmp/pyenv/bin/activate
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-'fci-admin'}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-'fci-admin@mail.com'}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-'fci@admin'}
APP_EXAMPLE_REPOSITORY="${GERRIT_URL}/helloworld"
APP_EXAMPLE_BUILD=${APP_EXAMPLE_BUILD:-'trunk'}
APP_EXAMPLE_PRODUCT=${APP_EXAMPLE_PRODUCT:-'my-product'}

cd /opt/apps/
python3 manage.py collectstatic
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py initsuperuser --username ${DJANGO_SUPERUSER_USERNAME} --email ${DJANGO_SUPERUSER_EMAIL} --password ${DJANGO_SUPERUSER_PASSWORD}
python3 manage.py initapp --repository ${APP_EXAMPLE_REPOSITORY} --build ${APP_EXAMPLE_BUILD} --product ${APP_EXAMPLE_PRODUCT}

uwsgi --ini uwsgi.ini

nginx -g 'daemon off;'
