FROM golang:1.21-alpine

WORKDIR /app

RUN apk add --no-cache \
    git \
    gcc \
    musl-dev \
    python3 \
    py3-pip \
    postgresql-client

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY go.mod go.sum ./
RUN go mod download

COPY . .

CMD ["sh", "-c", "go test ./... -v && python3 -m pytest tests/ -v"]
