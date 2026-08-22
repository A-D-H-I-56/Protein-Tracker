# ==============================================================================
# Self-Contained & Fully Configurable Production Dockerfile for NutriAI
# Zero hardcoded values: all parameters parameterized via ARG and ENV
# ==============================================================================
ARG PYTHON_VERSION=3.11-slim
FROM python:${PYTHON_VERSION} AS runner

# Build arguments with configurable defaults
ARG APP_USER=appuser
ARG APP_GROUP=appgroup
ARG APP_UID=10001
ARG APP_GID=10001
ARG PORT=5000
ARG HOST=0.0.0.0
ARG THREADS=4
ARG FLASK_ENV=production
ARG ARTIFACTS_DIR=/app/artifacts
ARG DATASET_PATH=/app/Fitness_data.csv

# Runtime environment variables mapped from ARGs (can be overridden at run time)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=${FLASK_ENV} \
    HOST=${HOST} \
    PORT=${PORT} \
    THREADS=${THREADS} \
    ARTIFACTS_DIR=${ARTIFACTS_DIR} \
    DATASET_PATH=${DATASET_PATH}

WORKDIR /app

# Install minimal system dependencies for health checks & clean cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create dedicated non-root security user & group dynamically
RUN groupadd -g ${APP_GID} ${APP_GROUP} && \
    useradd -u ${APP_UID} -g ${APP_GROUP} -s /bin/sh -m ${APP_USER}

# Layer caching for Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy entire project source code & dataset
COPY . .

# Ensure default .env fallback exists inside the container image
RUN if [ ! -f .env ]; then cp .env.example .env; fi

# Pre-train ML model & generate visual evaluation plots inside image during build
RUN python ml_pipeline/train.py && \
    python ml_pipeline/evaluate.py

# Ensure artifacts and app directories are owned by non-root user
RUN chown -R ${APP_USER}:${APP_GROUP} /app

# Switch to non-root user for runtime execution
USER ${APP_USER}

# Expose production port dynamically
EXPOSE ${PORT}

# Built-in container healthcheck using dynamic PORT variable
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:${PORT}/api/v1/health || exit 1

# Launch production WSGI server (Waitress)
CMD ["python", "wsgi.py"]
