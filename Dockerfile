FROM python:3
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app
CMD ["python", "/app/jungo_car_service.py"]
#CMD ["tail", "-f", "/dev/null"] #disable. cause docker logging not work.

