Instalación
===========
Para instalar y ejecutar este proyecto, puedes usar Docker o configurar un entorno de Python.

Usando Docker:
- Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
- Ejecuta `docker-compose up --build` para construir e iniciar los servicios. Esto configurará automáticamente el entorno necesario para ejecutar la aplicación.

Usando el entorno de Python:
- Crea un entorno virtual: `python -m venv env`
- Activa el entorno virtual: `source env/bin/activate`
- Instala las dependencias: `pip install -r requirements.txt`

Asegúrate de que todos los servicios necesarios, como GROBID, estén configurados y ejecutándose antes de iniciar la aplicación principal. 