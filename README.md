# 🍯 Easy Honeypot

Um honeypot SSH simples e eficaz para detectar tentativas de conexão e escaneamento de rede. Sistema completo com interface web para monitoramento em tempo real.

## 📋 Descrição

Este honeypot simula um servidor SSH na porta 2222 e registra automaticamente todas as tentativas de conexão, permitindo identificar possíveis atacantes, bots ou scanners de rede. Ideal para detectar atividades suspeitas em sua rede.

## 🏗️ Arquitetura

O sistema é composto por 3 containers Docker que se comunicam:

- **🐍 Backend (FastAPI)**: API REST para armazenar e consultar tentativas de conexão
- **⚛️ Frontend (React)**: Interface web moderna para visualização dos dados
- **🍯 Honeypot (Python)**: Servidor SSH falso que captura tentativas de conexão

## ✨ Funcionalidades

- ✅ Captura automática de tentativas de conexão SSH
- 📊 Dashboard web em tempo real
- 📈 Estatísticas de ataques (total de tentativas e IPs únicos)
- 🔄 Atualização automática dos dados
- 📱 Interface responsiva
- 🐳 Fácil deployment com Docker

## 🚀 Instalação e Uso

### Pré-requisitos

- Docker
- Docker Compose
- git

### Passos para executar

1. **Clone o repositório**:
```bash
git clone https://github.com/pedrosilvaevangelista/easy-honeypot.git
cd easy-honeypot
```

2. **Execute o script de inicialização**:
```bash
./start.sh
```

O script irá:
- Detectar automaticamente o IP da máquina
- Inicializar os containers Docker
- Exibir as URLs de acesso

### Acessando o sistema

Após a inicialização, você poderá acessar:

- **🌐 Interface Web**: `http://<ip-da-maquina>:3000`
- **🔧 API**: `http://<ip-da-maquina>:8000`
- **🍯 Honeypot SSH**: `<ip-da-maquina>:2222`

## 🧪 Testando o Honeypot

Para verificar se o sistema está funcionando, execute uma conexão SSH de teste:

### No Windows (CMD/PowerShell):
```cmd
ssh -p 2222 usuario@ip-da-maquina
```

### No Linux/macOS:
```bash
ssh -p 2222 usuario@ip-da-maquina
# ou
telnet ip-da-maquina 2222
# ou usando netcat
nc ip-da-maquina 2222
```

### Exemplo de simulação:
```bash
# Teste simulando scanner
nmap -p 2222 <ip-da-maquina>
```

Após executar qualquer um desses comandos, você deverá ver a tentativa registrada na interface web.

## 📊 Interface Web

O dashboard fornece:

- **📈 Estatísticas gerais**: Total de tentativas e IPs únicos
- **📋 Lista de tentativas**: Histórico detalhado com IP, dados da conexão e timestamp
- **🔄 Atualização automática**: Dados atualizados a cada 10 segundos
- **🎯 Status em tempo real**: Indicador de funcionamento do sistema


## 🔧 Configuração Avançada

### Personalizando a porta do honeypot

Para alterar a porta padrão (2222), edite o arquivo `honeypot/honeypot_ssh.py`:

```python
PORT = 2222  # Altere para a porta desejada
```

### Configurando logging

Os logs são automaticamente salvos e podem ser visualizados com:

```bash
# Ver logs do honeypot
docker-compose logs honeypot

# Ver logs do backend
docker-compose logs backend

# Ver todos os logs
docker-compose logs -f
```

## 🛡️ Segurança

⚠️ **Avisos importantes**:

- Este honeypot é apenas para **detecção e monitoramento**
- Não fornece proteção ativa contra ataques
- Execute apenas em ambientes controlados
- Monitore regularmente os logs para atividades suspeitas
- Considere implementar rate limiting para evitar DoS

## 🐛 Troubleshooting

### Container não inicia
```bash
# Verificar logs detalhados
docker-compose logs

# Reconstruir imagens
docker-compose build --no-cache
```

### Frontend não carrega dados
```bash
# Verificar se o backend está acessível
curl http://localhost:8000/health

# Verificar configuração de rede
docker-compose ps
```

### Tentativas não aparecem no dashboard
```bash
# Verificar logs do honeypot
docker-compose logs honeypot

# Testar conectividade do honeypot
telnet localhost 2222
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**📧 Suporte**: Para dúvidas ou problemas, abra uma issue no repositório.

**⭐ Star**: Se este projeto foi útil para você, considere dar uma estrela!
