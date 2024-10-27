FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev

RUN pip install --upgrade pip setuptools wheel

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD tail -f /dev/nullRUN pip install --upgrade pip
