.. Archivo maestro de documentación de Knowledge Graph SQL, creado por
   sphinx-quickstart el martes 27 de mayo de 2025.
   Puedes adaptar este archivo completamente a tu gusto, pero al menos debería
   contener la directiva raíz `toctree`.

Documentación de Knowledge Graph SQL
====================================

Introducción
------------
Este proyecto tiene como objetivo construir un grafo de conocimiento académico a partir de artículos científicos en formato PDF. El flujo de trabajo inicia con la extracción automática de información básica desde los archivos PDF mediante el servicio Grobid. Posteriormente, esta información se enriquece con datos adicionales provenientes de las plataformas OpenAIRE y OpenAlex, lo que permite vincular autores, organizaciones, proyectos y otras entidades relevantes.

Instalación
-----------
Para instalar y ejecutar este proyecto, puedes usar Docker o configurar un entorno Python.

**Usando Docker**

Asegúrate de tener Docker y Docker Compose instalados en tu sistema. Luego, ejecuta:

.. code-block:: bash

   docker-compose up --build

**Usando entorno Python**

1. Crea un entorno virtual:

   .. code-block:: bash

      python -m venv env

2. Activa el entorno virtual:

   .. code-block:: bash

      source env/bin/activate

3. Instala las dependencias:

   .. code-block:: bash

      pip install -r requirements.txt

Uso
---
Después de la instalación, puedes ejecutar la aplicación principal usando:

- `python src/main.py` para ejecución directa.
- O bien, accede a la aplicación Streamlit ejecutando:

  .. code-block:: bash

     streamlit run src/app.py

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
