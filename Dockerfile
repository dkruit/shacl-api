FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY shaclapi/ shaclapi/
COPY tests/ tests/

CMD ["flask", "--app", "shaclapi/api", "run", "--host=0.0.0.0"]
