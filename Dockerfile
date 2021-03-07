FROM python:3.8.4
#RUN pip install requests
#RUN apt-get -qq -y install curl
COPY . /app
WORKDIR /app
EXPOSE 8888

ENTRYPOINT ["python", "./app.py"]