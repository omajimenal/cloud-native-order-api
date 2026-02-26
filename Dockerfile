# -------- BUILD STAGE --------
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --prefix=/install -r requirements.txt

# -------- RUNTIME STAGE --------
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN useradd -m appuser

COPY --from=builder /install /usr/local
COPY app/ .

USER appuser

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]