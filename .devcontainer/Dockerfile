FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# O cliente MySQL permite que o aluno teste e importe o banco pelo terminal.
# O servidor MySQL roda em outro contêiner definido no compose.yaml.
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends default-mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
