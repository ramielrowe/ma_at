FROM python:3

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD . /ma_at/
WORKDIR /ma_at/
RUN python setup.py install

ENTRYPOINT ["ma_at"]
