FROM nginx:alpine

RUN apk update \
    && apk add openssl

COPY nginx.conf.template /etc/nginx/templates/
COPY make_auth.sh /docker-entrypoint.d/

RUN rm /etc/nginx/conf.d/default.conf \
    && mkdir -p /etc/mlflow/ \
    && chmod +x /docker-entrypoint.d/make_auth.sh
