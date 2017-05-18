FROM alpine
LABEL maintainer "Alex Chan alex@alexwlchan.net"

RUN apk update
RUN apk add nginx python3 supervisor uwsgi uwsgi-python3
RUN apk add build-base python3-dev jpeg-dev zlib-dev
RUN pip3 install --upgrade pip

EXPOSE 80

# NGINX config: run in the background with custom configuration
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

COPY flask_requirements.txt /flask_requirements.txt
RUN pip3 install -r /flask_requirements.txt
RUN pip3 install specktre

COPY flaskapp /flaskapp

COPY nginx.conf /etc/nginx/conf.d/
RUN mkdir -p /run/nginx
COPY uwsgi.ini /etc/uwsgi
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
