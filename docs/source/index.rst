.. Archivo maestro de documentación de Knowledge Graph SQL, creado por
   sphinx-quickstart el martes 27 de mayo de 2025.
   Puedes adaptar este archivo completamente a tu gusto, pero al menos debería
   contener la directiva raíz `toctree`.

Documentación de Knowledge Graph SQL
=====================================

Introducción
------------
Este proyecto está diseñado para crear y gestionar un grafo de conocimiento utilizando bases de datos SQL. Proporciona herramientas para extraer, enriquecer y visualizar datos de artículos académicos y proyectos relacionados.

Instalación
------------
Para instalar y ejecutar este proyecto, puedes usar Docker o configurar un entorno Python.

Usando Docker:
- Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
- Ejecuta `docker-compose up --build` para construir e iniciar los servicios.

Usando Entorno Python:
- Crea un entorno virtual: `python -m venv env`
- Activa el entorno virtual: `source env/bin/activate`
- Instala las dependencias: `pip install -r requirements.txt`

Uso
---
Después de la instalación, puedes ejecutar la aplicación principal usando:
- `python src/main.py` para ejecución directa.
- Accede a la aplicación Streamlit ejecutando `streamlit run src/app.py`.

Resultados
----------
La aplicación generará un grafo de conocimiento que puede ser visualizado y exportado al formato RDF. La aplicación Streamlit proporciona vistas interactivas para explorar los datos.

.. toctree::
   :maxdepth: 2
   :caption: Contenidos:

   introduccion
   instalacion
   uso
   resultados
   modules

