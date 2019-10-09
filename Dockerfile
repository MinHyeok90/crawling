FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "/app/crawling.py"]
#CMD ["tail", "-f", "/dev/null"] #disable. cause docker logging not work.

