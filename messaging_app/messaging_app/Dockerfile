# messaging_app/Dockerfile

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Use Gunicorn with `-p`-like argument (`--bind`)
CMD ["gunicorn", "my_django_app.wsgi:application", "--bind", "0.0.0.0:8000"]
