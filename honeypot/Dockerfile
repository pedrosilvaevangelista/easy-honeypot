FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
RUN pip install --no-cache-dir requests

# Copiar arquivo do honeypot
COPY honeypot_ssh.py /app/

# Expor porta do SSH falso
EXPOSE 2222

# Comando para executar o honeypot
CMD ["python", "-u", "honeypot_ssh.py"]
