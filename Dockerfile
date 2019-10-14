FROM python:3
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN pip uninstall python-telegram-bot -y
RUN pip install python-telegram-bot
ADD . /app
ENTRYPOINT ["python3"]
CMD ["./app/jungo_car_service.py"]
#CMD ["tail", "-f", "/dev/null"] #disable. cause docker logging not work.

