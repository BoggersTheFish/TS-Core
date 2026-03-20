# TS-Core v1.0 — Python runtime (Rust optional on host via maturin/cargo).
FROM python:3.12-slim-bookworm

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TSCORE_HOME=/data/tscore

COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests

RUN pip install --upgrade pip && pip install -e ".[dev,gui]"

RUN mkdir -p /data/tscore
VOLUME ["/data/tscore"]

CMD ["python", "-m", "src.python.mind_runtime", "--demo"]
