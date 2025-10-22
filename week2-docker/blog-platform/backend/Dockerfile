FROM python:3.9-alpine

RUN apk add --no-cache gcc musl-dev postgresql-dev libpq

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
