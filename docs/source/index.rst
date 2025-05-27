.. Knowledge Graph SQL documentation master file, created by
   sphinx-quickstart on Tue May 27 09:19:27 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Knowledge Graph SQL documentation
=================================

Introduction
------------
This project is designed to create and manage a knowledge graph using SQL databases. It provides tools for extracting, enriching, and visualizing data from academic papers and related projects.

Installation
------------
To install and run this project, you can use Docker or set up a Python environment.

Using Docker:
- Ensure you have Docker and Docker Compose installed on your system.
- Run `docker-compose up --build` to build and start the services.

Using Python Environment:
- Create a virtual environment: `python -m venv env`
- Activate the virtual environment: `source env/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

Usage
-----
After installation, you can run the main application using:
- `python src/main.py` for direct execution.
- Access the Streamlit app by running `streamlit run src/app.py`.

Results
-------
The application will generate a knowledge graph that can be visualized and exported to RDF format. The Streamlit app provides interactive views for exploring the data.

.. toctree::
   :maxdepth: 2
   :caption: Contenidos:

   introduccion
   instalacion
   uso
   resultados
   modules

