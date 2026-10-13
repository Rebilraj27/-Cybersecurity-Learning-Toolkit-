# =============================================================================
# Cyber Toolkit — Dockerfile
# Created by: Rebilraj
# =============================================================================

# ─── Stage 1: Builder ────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build deps for cryptography / scapy
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpcap-dev \
        libssl-dev \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps into a virtualenv we can copy
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip wheel setuptools \
    && pip install --no-cache-dir -r requirements.txt


# ─── Stage 2: Runtime ────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

LABEL org.opencontainers.image.title="Cyber Toolkit" \
      org.opencontainers.image.description="Python-based cybersecurity learning toolkit" \
      org.opencontainers.image.authors="Rebilraj" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.version="1.0.0"

# Runtime libs only (libpcap for scapy, tcpdump for debugging)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpcap0.8 \
        tcpdump \
        iputils-ping \
        net-tools \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Non-root user for safety
RUN groupadd --gid 1000 cyber \
    && useradd --uid 1000 --gid cyber --create-home --shell /bin/bash cyber

WORKDIR /app
COPY --chown=cyber:cyber . .

# Make entrypoint executable
RUN chmod +x /app/docker/entrypoint.sh

# Drop privileges
USER cyber

ENTRYPOINT ["/app/docker/entrypoint.sh"]
CMD ["--help"]
