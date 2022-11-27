FROM python:3

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY .  /app

EXPOSE 5000

CMD ["python", "./app.py"]