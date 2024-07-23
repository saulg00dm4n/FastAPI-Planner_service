FROM python:3.12-slim


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install -r requirements.txt


CMD ["uvicorn", "--port", "8001", "--host", "0.0.0.0", "main:app"]