FROM python:3.6.8
WORKDIR /root
RUN pip install --upgrade pip
COPY ./requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt
ADD . /root
ENTRYPOINT ["python3"]
CMD ["./app/src/jungo_car_service.py"]
#CMD ["tail", "-f", "/dev/null"] #disable. cause docker logging not work.

