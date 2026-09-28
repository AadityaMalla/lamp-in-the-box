FROM nginx:stable-alpine
ENV ROCKET_HOST=127.0.0.1
COPY default.conf.template /etc/nginx/templates/default.conf.template
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
