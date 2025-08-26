# Usar una imagen de Python oficial.
FROM python:3.9-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Exponer el puerto que usa la aplicación
EXPOSE 8000

# Comando para correr la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api_server:app"]
