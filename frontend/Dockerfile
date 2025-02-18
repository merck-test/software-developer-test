# Usa Python 3.9 como imagen base
FROM python:3.9

# Define el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias antes para aprovechar la caché de Docker
COPY requirements.txt .

# Instala las dependencias sin caché
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la aplicación
COPY . .

# Comando para ejecutar Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
