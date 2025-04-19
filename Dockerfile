FROM python:3.13-alpine3.21

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install Flask pygal requests pandas matplotlib

COPY . .

CMD ["python", "run.py"]