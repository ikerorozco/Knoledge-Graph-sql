# Usa imagen oficial de Python
FROM python:3.9

# Define directorio de trabajo
WORKDIR /app

# Copia y luego instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia toda la carpeta src para que esté disponible app.py y demás
COPY src/ ./src/

# Expone puerto 8501 (puerto por defecto de Streamlit)
EXPOSE 8501

# Comando para ejecutar Streamlit con la app
CMD [ "Python","src/main.py" ]
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
