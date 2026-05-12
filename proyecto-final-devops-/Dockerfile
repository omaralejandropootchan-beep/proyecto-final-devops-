# Imagen base ligera
FROM python:3.9-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY app.py .

# Instalar dependencias necesarias
RUN pip install flask

# Exponer el puerto
EXPOSE 80

# Comando para iniciar la app
CMD ["python", "app.py"]
