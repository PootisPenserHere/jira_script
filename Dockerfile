FROM python:2.7.15-alpine
LABEL maintainer "josepablo.aramburo@laziness.rocks"

ARG BASE_URL
ARG USER_NAME
ARG API_KEY

ENV BASE_URL=$BASE_URL
ENV USER_NAME=$USER_NAME
ENV API_KEY=$API_KEY

ADD . /code
WORKDIR /code
VOLUME /code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#ENTRYPOINT ["python"]
CMD ["jira.py"]
