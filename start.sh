#!/bin/bash

# Script para iniciar o honeypot com o IP correto da máquina

# Detectar IP da máquina
HOST_IP=$(hostname -I | awk '{print $1}')

# Se não conseguir detectar, usar um IP padrão
if [ -z "$HOST_IP" ]; then
    HOST_IP=$(ip route get 8.8.8.8 | awk '{print $7; exit}')
fi

# Se ainda não conseguir, tentar outra forma
if [ -z "$HOST_IP" ]; then
    HOST_IP=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | head -n1)
fi

echo "🔍 Detectando IP da máquina..."
echo "📡 IP detectado: $HOST_IP"
echo ""

# Exportar a variável de ambiente
export HOST_IP=$HOST_IP

echo "🚀 Iniciando honeypot..."
echo "📊 Dashboard estará disponível em: http://$HOST_IP:3000"
echo "🔧 API estará disponível em: http://$HOST_IP:8000"
echo "🍯 Honeypot SSH estará na porta: $HOST_IP:2222"
echo ""

# Parar containers existentes
docker-compose down

# Iniciar com o IP correto
docker-compose up --build

echo ""
echo "✅ Para acessar de outras máquinas:"
echo "   Frontend: http://$HOST_IP:3000"
echo "   API: http://$HOST_IP:8000"
echo "   SSH Honeypot: $HOST_IP:2222"
