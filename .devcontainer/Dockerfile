FROM mcr.microsoft.com/devcontainers/cpp:1-ubuntu-24.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 less man-db \
    && rm -rf /var/lib/apt/lists/*
