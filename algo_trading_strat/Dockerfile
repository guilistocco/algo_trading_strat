FROM python:3.10-slim

WORKDIR /app

COPY ./shared ./shared
COPY ./docker/${STRATEGY}/ ./strategy
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "strategy/run.py"]