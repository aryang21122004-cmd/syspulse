# ── Stage 1: Builder ──────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/deps --no-cache-dir -r requirements.txt


# ── Stage 2: Runtime ──────────────────────────────────────────────
FROM python:3.11-slim

RUN useradd -m appuser
WORKDIR /app

COPY --from=builder /deps /usr/local
COPY app.py .
COPY templates/ ./templates/

# ... (Your existing COPY commands for app.py, templates, static) ...
COPY app.py .
COPY templates/ ./templates/

# ADD THIS LINE: Give appuser permission to write to the app directory
RUN chown -R appuser:appuser /app

# This is where it switches to the restricted user
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

USER appuser
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60"]
