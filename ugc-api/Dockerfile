FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get -y update && apt-get -y install build-essential && apt-get -y install kafkacat
COPY src/requirements.txt /code/
RUN pip install -r requirements.txt
COPY src/ /code/
EXPOSE 8000
CMD sh wait-for-kafka.sh
