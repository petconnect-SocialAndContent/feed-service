# Usa una imagen oficial mínima de Python
FROM python:3.11-slim

# Define variables para producción y codificación
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para algunas librerías (como redis, flask, pymongo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala solo requirements (mejor caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la app
COPY . .

# Expone el puerto definido en tu .env (3010)
EXPOSE 3010

# Comando de inicio
CMD ["python", "app.py"]
