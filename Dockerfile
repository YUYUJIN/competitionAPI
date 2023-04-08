FROM python:3.8.0

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ADD . /app

EXPOSE 5000

CMD python ./app.py