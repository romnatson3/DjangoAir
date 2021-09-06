FROM python:3

WORKDIR /romair

COPY requirements.txt /romair

RUN pip install --no-cache-dir -r requirements.txt

COPY . /romair
