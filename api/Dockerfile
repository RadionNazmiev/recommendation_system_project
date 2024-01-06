FROM python:3.8.5-slim-buster

WORKDIR /api

COPY ../requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]















