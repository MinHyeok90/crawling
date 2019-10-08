# docker build --tag jungo-alarmer:2 .
FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python ./crawling.py

