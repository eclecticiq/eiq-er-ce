#!/bin/bash
echo "Starting docker entry point script..."


echo "Waiting for PostgreSQL to start..."

until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_ADDRESS -U $POSTGRES_USER -d $POSTGRES_DB_NAME -c "select 1" > /dev/null 2>&1 ; do
  sleep 5
done


file="/tmp/celerybeat.pid"

if [ -f $file ] ; then
    rm $file
fi


TARGET=/usr/local/lib/python3.7/site-packages/celery/backends
cd $TARGET
if [ -e async.py ]
then
    mv async.py asynchronous.py
    sed -i 's/async/asynchronous/g' redis.py
    sed -i 's/async/asynchronous/g' rpc.py
fi
CORES=1
if [[ "$OSTYPE" == "linux-gnu" ]]; then
        CORES="$(nproc --all)"
elif [[ "$OSTYPE" == "darwin"* ]]; then
        CORES="$(sysctl -n hw.ncpu)"
elif [[ "$OSTYPE" == "cygwin" ]]; then
		echo "Os is cygwin.."
        # POSIX compatibility layer and Linux environment emulation for Windows
elif [[ "$OSTYPE" == "msys" ]]; then
		echo "Os is msys.."
        # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
elif [[ "$OSTYPE" == "win32" ]]; then
		CORES=echo %NUMBER_OF_PROCESSORS%
        # I'm not sure this can happen.
elif [[ "$OSTYPE" == "freebsd"* ]]; then
        CORES="$(sysctl -n hw.ncpu)"
 else
		echo "Os is unknown.."
fi
cd /src/plgx-esp
[ -f resources/certificate.crt ] && echo "PolyLogyx fleet is configured for SSL" || echo "PolyLogyx Fleet is not configured for SSL, please run certificate-generate.sh or use OpenSSL to create key pair. Check deployment guide for more info..."

echo "Creating enroll file..."
exec `echo "$ENROLL_SECRET">resources/secret.txt`

echo "Creating celery tmux sessions..."
exec `tmux new-session -d -s plgx_celery`
exec `tmux new-session -d -s plgx_celery_beat`
exec `tmux new-session -d -s plgx_gunicorn`
\exec `tmux new-session -d -s flower`




CORES="$(nproc --all)"
echo "CPU cores are $CORES"
WORKERS=$(( 2*CORES+1  ))
WORKERS_CELERY=$(( 2*CORES  ))


echo "Creating DB schema..."
python manage.py db upgrade

echo "Creating default user..."
exec `tmux send -t plgx_celery 'python manage.py add_user  "$POLYLOGYX_USER" --password  "$POLYLOGYX_PASSWORD"' ENTER`

echo "Adding default configs..."
exec `tmux send -t plgx_celery 'python manage.py add_default_config default_config_windows --filepath default_data/default_configs/default_config_windows_shallow.conf --platform windows' ENTER`
exec `tmux send -t plgx_celery 'python manage.py add_default_config default_config_windows --filepath default_data/default_configs/default_config_windows_deep.conf --platform windows' ENTER`

exec `tmux send -t plgx_celery 'python manage.py add_default_config default_config_macos --filepath default_data/default_configs/default_config_macos.conf --platform darwin' ENTER`
exec `tmux send -t plgx_celery 'python manage.py add_default_config default_config_linux --filepath default_data/default_configs/default_config_linux.conf --platform linux' ENTER`
exec `tmux send -t plgx_celery 'python manage.py add_default_config default_config_freebsd --filepath default_data/default_configs/default_config_freebsd.conf --platform freebsd' ENTER`
exec `tmux send -t plgx_celery 'python manage.py add_default_options' ENTER`


exec `tmux send -t plgx_celery 'python manage.py delete_existing_unmapped_queries_filters' ENTER`


echo "Adding default filters..."
exec `tmux send -t plgx_celery 'python manage.py add_default_filters --filepath default_data/default_filters/default_filter_linux.conf --platform linux' ENTER`
exec `tmux send -t plgx_celery 'python manage.py add_default_filters --filepath default_data/default_filters/default_filter_macos.conf --platform darwin' ENTER`
exec `tmux send -t plgx_celery 'python manage.py add_default_filters --filepath default_data/default_filters/default_filter_windows_shallow.conf --platform windows --type 1' ENTER`
exec `tmux send -t plgx_celery 'python manage.py add_default_filters --filepath default_data/default_filters/default_filter_windows_deep.conf --platform windows --type 2' ENTER`

exec `tmux send -t plgx_celery 'python manage.py add_default_filters --filepath default_data/default_filters/default_filter_windows_x86.conf --platform windows --arch x86' ENTER`

echo "Adding default queries..."
exec `tmux send -t plgx_celery 'python manage.py add_default_queries --filepath default_data/default_queries/default_queries_linux.conf --platform linux' ENTER`
exec `tmux send -t plgx_celery 'python manage.py add_default_queries --filepath default_data/default_queries/default_queries_macos.conf --platform darwin' ENTER`
exec `tmux send -t plgx_celery 'python manage.py add_default_queries --filepath default_data/default_queries/default_queries_windows_shallow.conf --platform windows --type 1' ENTER`
exec `tmux send -t plgx_celery 'python manage.py add_default_queries --filepath default_data/default_queries/default_queries_windows_deep.conf --platform windows --type 2' ENTER`

exec `tmux send -t plgx_celery 'python manage.py add_default_queries --filepath default_data/default_queries/default_queries_windows_x86.conf --arch x86 --platform windows' ENTER`

echo "Adding released version's agent information..."
exec `tmux send -t plgx_celery 'python manage.py add_release_versions --filepath default_data/platform_releases.conf' ENTER`


echo "Adding default mitre rules..."
for entry in /src/plgx-esp/default_data/mitre-attack/*
do
  packname=$(basename "$entry" .json)
  echo $packname
  exec `tmux send -t plgx_celery 'python manage.py add_rules  --filepath '"$entry" ENTER`
done

echo "Adding default query packs..."
for entry in /src/plgx-esp/default_data/packs/*
do
  packname=$(basename "$entry" .conf)
  echo $packname
  exec `tmux send -t plgx_celery 'python manage.py addpack ' $packname ' --filepath '"$entry" ENTER`
done

cd /src/plgx-esp
echo "Starting celery beat..."
exec `tmux send -t plgx_celery_beat 'celery beat -A polylogyx.worker:celery --schedule=/tmp/celerybeat-schedule --loglevel=INFO --logfile=/var/log/celery-beat.log --pidfile=/tmp/celerybeat.pid' ENTER`
echo "Starting celery RabbitMQ..."


echo "Starting PolyLogyx Vasp osquery fleet manager..."
exec `tmux send -t plgx_gunicorn "gunicorn -w $WORKERS -k gevent --worker-connections 40 --log-level 'warning' --access-logfile '/var/log/gunicorn-access.log' --error-logfile '/var/log/gunicorn-error.log' --capture-output --timeout 120 --bind 0.0.0.0:6000   manage:app --reload" ENTER`

if [[ -z "$PURGE_DATA_DURATION" ]]
then
  echo "PURGE_DATA_DURATION value is not set, data will not be purged automatically!"
else
  echo "Creating platform settings..."
  exec `tmux send -t plgx_celery 'python manage.py update_settings --purge_data_duration '"$PURGE_DATA_DURATION" ENTER`
fi

exec `tmux send -t plgx_celery 'python manage.py add_default_vt_av_engines --filepath default_data/Virustotal-avengines/default_VT_Av_engines.json' ENTER`

exec `tmux send -t plgx_celery 'python manage.py  update_vt_match_count --vt_min_match_count '"$VT_MIN_MATCH_COUNT" ENTER`

echo "Updating OSQuery Schema from polylogyx/resources/osquery_schema.json ..."
exec `tmux send -t plgx_celery "python manage.py update_osquery_schema --file_path polylogyx/resources/osquery_schema.json " ENTER`

exec `tmux send -t plgx_celery "celery worker -A polylogyx.worker:celery --concurrency=$WORKERS_CELERY -Q default_queue_tasks --loglevel=INFO --logfile=/var/log/celery.log &" ENTER`

echo "Sever is up and running.."
exec `tmux send -t flower "flower -A polylogyx.worker:celery --address=0.0.0.0  --broker_api=http://guest:guest@$RABBITMQ_URL:5672/api --basic_auth=$POLYLOGYX_USER:$POLYLOGYX_PASSWORD" ENTER`

exec `tail -f /dev/null`
