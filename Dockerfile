FROM python:2.7.12

RUN rm -f /etc/localtime && ln -s /usr/share/zoneinfo/Australia/Melbourne /etc/localtime
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ADD requirements.txt /code/requirements.txt

RUN virtualenv venv

RUN /bin/bash -c "source /venv/bin/activate && \
    pip install -r /code/requirements.txt"