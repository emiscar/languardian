# Dockerfile

FROM python:3.9

# install nginx
RUN apt-get update && apt-get install nginx vim git -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# copy source and install dependencies

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
#RUN mkdir -p /opt/app/languardian
COPY requirements.txt start-server.sh /opt/app/
COPY .pip_cache /opt/app/pip_cache/
#COPY . /opt/app/languardian/
RUN git clone "https://github.com/emiscar/languardian.git" /opt/app/languardian/
WORKDIR /opt/app
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app
RUN chown -R www-data:www-data /root

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]