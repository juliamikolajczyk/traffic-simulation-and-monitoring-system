FROM python:3.14.7-slim-trixie AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
RUN /opt/venv/bin/python -m pip install --no-cache-dir requirements.txt

FROM python:3.14.7-slim-trixie AS runner
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . .
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

RUN useradd -u 1234 generator && chown generator:generator -R /app && chmod 555 -R /app
USER generator

ENTRYPOINT ["python", "main.py"]
