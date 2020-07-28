FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    locales vim python3 python3-pip git libpq-dev libevent-dev uwsgi-plugin-python3\
    supervisor

ENV LANG C.UTF-8

# Install virtual environment
RUN pip3 install virtualenv

RUN useradd -ms /bin/bash emp-portal
USER emp-portal

# Environment variables
ENV HOME /home/emp-portal
ENV APP $HOME/EMApp
ENV PY_ENV /home/emp-portal/emp_env
ENV CONFIG_DIR $HOME/etc
ENV EXTENSIONS $APP/extensions
ENV PATH $PY_ENV/bin:$PATH

ENV PORT 8800
WORKDIR $APP

# Create and activate environment variables
RUN python3 -m virtualenv --python=/usr/bin/python3 $PY_ENV
RUN virtualenv $PY_ENV

# Copy dir and settings
ADD --chown=emp-portal:emp-portal ./etc/ $CONFIG_DIR
ADD --chown=emp-portal:emp-portal ./EMApp/ $HOME/EMApp

ENV YAMLCONF_CONFFILE $CONFIG_DIR/config.yaml

# Install all necessary django packages
RUN $PY_ENV/bin/pip3 install -r $APP/app/requirements.txt

# Install core app and its requirements
RUN cd $APP/app/ && $PY_ENV/bin/python -m pip install -r indirect-requirements.txt

# Install all the extensions and its dependencies
RUN cd $EXTENSIONS && $PY_ENV/bin/python -m pip install -r $EXTENSIONS/requirements.txt

EXPOSE $PORT

CMD ["/home/emp-portal/emp_env/bin/uwsgi", "--ini", "/home/emp-portal/etc/uwsgi.ini"]

