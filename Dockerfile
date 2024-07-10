FROM python:3.11-slim

EXPOSE 8080
ENV PORT 8080

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD python main.py