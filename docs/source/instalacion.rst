Instalación
===========
Para instalar y ejecutar este proyecto, puedes usar Docker o configurar un entorno de Python.

Usando Docker:
- Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
- Ejecuta::

.. code-block:: bash

    docker-compose up --build

Usando el entorno de Python:
- Crea un entorno virtual::

.. code-block:: bash

    python -m venv env

- Activa el entorno virtual::

.. code-block:: bash

    source env/bin/activate

- Instala las dependencias::

.. code-block:: bash

    pip install -r requirements.txt

Asegúrate de que todos los servicios necesarios, como GROBID, estén configurados y ejecutándose antes de iniciar la aplicación principal. 