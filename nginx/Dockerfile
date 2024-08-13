FROM nginx:alpine 

# install dockerize
# https://github.com/jwilder/dockerize
RUN apk add --no-cache openssl
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz


WORKDIR /app/nginx

COPY default.temp.conf ./default.temp.conf
COPY uwsgi_params ./uwsgi_params

RUN echo "daemon off;" >> /etc/nginx/nginx.conf