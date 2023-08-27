#! /bin/sh
set -e

/usr/envsubst < /etc/prometheus/prometheus.yml.template > /etc/prometheus/prometheus.yml
cat /etc/prometheus/prometheus.yml
/bin/prometheus \
    --config.file=/etc/prometheus/prometheus.yml \
    --storage.tsdb.path=/prometheus \
    --web.console.libraries=/usr/share/prometheus/console_libraries \
    --web.console.templates=/usr/share/prometheus/consoles \
    --web.enable-lifecycle