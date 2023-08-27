FROM prom/prometheus:latest
USER root

COPY ./prometheus-start.sh /usr/prometheus-start.sh

RUN set -e \
    && wget -O /usr/envsubst https://github.com/a8m/envsubst/releases/download/v1.4.2/envsubst-Linux-x86_64 \
    && chmod +x /usr/envsubst \
    && chmod +x /usr/prometheus-start.sh

COPY ./prometheus.yml.template /etc/prometheus/
WORKDIR /prometheus
ENTRYPOINT [ "/usr/prometheus-start.sh" ]