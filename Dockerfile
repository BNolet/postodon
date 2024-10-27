FROM python:3-bookworm

COPY ./src/ /app/src/
COPY requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r /app/requirements.txt

CMD ["python", "/app/src/app.py"]