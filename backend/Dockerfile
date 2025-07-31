FROM python:3.11-slim

WORKDIR /app

# Instalar curl para healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Criar diretório de dados com permissões corretas
RUN mkdir -p /app/app/data && \
    chmod 755 /app/app/data

# Expor porta
EXPOSE 8000

# Comando de inicialização sem logs excessivos
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "warning"]
