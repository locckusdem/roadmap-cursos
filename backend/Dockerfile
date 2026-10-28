# Stage 1: Builder
FROM python:3.12-alpine AS builder

WORKDIR /app
RUN apk add --no-cache binutils
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project && \
    find /app/.venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -name "*.so" -exec strip --strip-unneeded {} + 2>/dev/null || true

# Stage 2: Runtime ultra liviano (< 100 MB)
FROM python:3.12-alpine AS runtime

WORKDIR /app

# Crear usuario appuser sin privilegios (no-root)
RUN adduser -D -u 1000 appuser

# Copiar exclusivamente el virtualenv y código de app/
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY app/ /app/app/

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
