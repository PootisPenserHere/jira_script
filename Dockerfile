FROM python:2.7.15-alpine
LABEL maintainer "josepablo.aramburo@laziness.rocks"

ENV PATH /usr/bin/python:$PATH

ADD . /code
WORKDIR /code
VOLUME /code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["jira.py"]
