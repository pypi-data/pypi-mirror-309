FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

COPY . /app
WORKDIR /app

RUN uv venv \
    && . .venv/bin/activate \
    && uv pip install torch --index-url https://download.pytorch.org/whl/cpu \
    && uv pip install . \
    && uv cache clean

ENV PATH="/app/.venv/bin:$PATH"
