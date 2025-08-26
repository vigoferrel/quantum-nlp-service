# Dockerfile para el servicio Ollama Worker

FROM node:18-slim

WORKDIR /usr/src/app

# Copiar el package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el código del worker
COPY worker.js .

# Ejecutar el worker
CMD [ "node", "worker.js" ]
