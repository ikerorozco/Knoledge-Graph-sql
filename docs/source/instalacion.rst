============
Instalación
============

Esta guía te llevará paso a paso a través del proceso de instalación de Knowledge Graph.


🚀 Métodos de Instalación
=========================

Método 1: Docker (Recomendado)
-------------------------------

Docker es la opción más simple y confiable para ejecutar Knowledge Graph SQL.

**Paso 1: Instalar Docker**

.. tabs::

   .. code-tab:: bash Linux (Ubuntu/Debian)

      # Actualizar el sistema
      sudo apt update
      sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release

      # Agregar clave GPG oficial de Docker
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

      # Agregar repositorio Docker
      echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

      # Instalar Docker
      sudo apt update
      sudo apt install docker-ce docker-ce-cli containerd.io docker-compose

   .. code-tab:: bash macOS

      # Instalar Homebrew si no está instalado
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

      # Instalar Docker Desktop
      brew install --cask docker

   .. code-tab:: bash Windows

      # Descargar Docker Desktop desde:
      # https://www.docker.com/products/docker-desktop

**Paso 2: Clonar el Repositorio**

.. code-block:: bash

   git clone https://github.com/ikerorozco/Knoledge-Graph-sql
   cd Knowledge-Graph-SQL


**Paso 4: Ejecutar con Docker Compose**

.. code-block:: bash

   # Construir y ejecutar
   docker-compose up --build -d

   # Verificar que los servicios estén ejecutándose
   docker-compose ps

.. note::
   La primera ejecución puede tomar varios minutos mientras se descargan las dependencias.

Método 2: Instalación Local con Python
---------------------------------------

Para desarrolladores que prefieren un entorno de desarrollo local.

**Paso 1: Verificar Python**

.. code-block:: bash

   python --version
   # Debe mostrar Python 3.8 o superior

**Paso 2: Clonar el Repositorio**

.. code-block:: bash

   git clone https://github.com/ikerorozco/Knoledge-Graph-sql
   cd Knowledge-Graph-SQL

**Paso 3: Crear Entorno Virtual**

.. tabs::

   .. code-tab:: bash Linux/macOS

      # Crear entorno virtual
      python -m venv knowledge_graph_env

      # Activar entorno virtual
      source knowledge_graph_env/bin/activate

   .. code-tab:: bash Windows

      # Crear entorno virtual
      python -m venv knowledge_graph_env

      # Activar entorno virtual
      knowledge_graph_env\Scripts\activate

**Paso 4: Instalar Dependencias**

.. code-block:: bash

   # Actualizar pip
   pip install --upgrade pip

   # Instalar dependencias principales
   pip install -r requirements.txt
