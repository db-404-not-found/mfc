FROM nginx:alpine

RUN mkdir -p /var/logs/nginx/backend/ && rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d/