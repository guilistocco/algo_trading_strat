FROM python:3.10-slim

WORKDIR /app

COPY ../../shared ./shared
COPY ./run.py .

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]