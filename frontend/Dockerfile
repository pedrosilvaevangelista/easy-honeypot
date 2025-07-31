FROM node:18-alpine

WORKDIR /app

# 1. Copia apenas o package.json primeiro
COPY package.json .

# 2. Gera o package-lock.json se não existir
RUN if [ ! -f package-lock.json ]; then \
      npm install --package-lock-only --no-audit --progress=false; \
    fi

# 3. Instala as dependências
RUN npm install --silent

# 4. Copia o restante dos arquivos
COPY . .

ENV REACT_APP_API_URL=http://backend:8000
ENV REACT_APP_WS_URL=ws://backend:8000

CMD ["npm", "start"]
