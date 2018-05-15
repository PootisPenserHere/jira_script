FROM python:3.5-alpine
LABEL maintainer "josepablo.aramburo@laziness.rocks"
ADD . /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

