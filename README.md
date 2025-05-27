[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15529403.svg)](https://doi.org/10.5281/zenodo.15529403)

# Knowledge Graph

## 🎯 Introducción

Este proyecto tiene como objetivo construir un **grafo de conocimiento académico** a partir de artículos científicos en formato PDF. La aplicación implementa un flujo de trabajo completo que:

1. **Extrae información automáticamente** desde archivos PDF mediante el servicio **Grobid**
2. **Enriquece los datos** con información adicional de plataformas como **OpenAIRE** y **OpenAlex**
3. **Vincula autores, organizaciones, proyectos** y otras entidades relevantes
4. **Realiza análisis semántico** de los resúmenes utilizando modelos de lenguaje de **Hugging Face**
5. **Identifica similitudes temáticas** entre diferentes papers
6. **Construye un grafo de conocimiento estructurado** con relaciones entre publicaciones, autores, instituciones y proyectos

## ✨ Características

### 🔍 Procesamiento de Documentos
- **Extracción automática de metadatos** desde PDFs usando Grobid
- **Análisis semántico de abstracts** con modelos de Hugging Face
- **Enriquecimiento de datos** desde OpenAIRE y OpenAlex

### 🌐 Visualización Interactiva
- **Red Interactiva**: Visualiza el grafo de conocimiento con nodos y relaciones
- **Autores por Paper**: Muestra los autores asociados a cada publicación
- **Buscador de Papers**: Permite buscar publicaciones por palabras clave en títulos
- **Línea de Tiempo de Proyectos**: Presenta un diagrama de Gantt de los proyectos
- **Mapa de Organizaciones**: Muestra un mapa geográfico de las organizaciones involucradas

### 📊 Exportación y Interoperabilidad
- **Exportación a formato RDF** para interoperabilidad con sistemas semánticos
- **Consultas personalizadas** sobre el grafo de conocimiento
- **Visualización dinámica** de resultados

## 🏗️ Arquitectura del Proyecto

```
Knowledge-Graph-SQL/
├── src/                    # Código fuente principal
│   ├── extractors/         # Módulos de extracción de datos
│   ├── api/               # Interfaces API (OpenAIRE, OpenAlex)
│   ├── models/            # Modelos de datos y entidades
│   ├── graph/             # Construcción del grafo de conocimiento
│   ├── views/             # Vistas de Streamlit
│   ├── main.py            # Aplicación principal
│   └── app.py             # Aplicación Streamlit
├── docs/                  # Documentación ReadTheDocs
│   ├── source/            # Archivos fuente de documentación
│   └── build/             # Documentación compilada
├── data/                  # Datos de entrada y procesados
├── tests/                 # Pruebas unitarias
└── backup/                # Respaldos
```

## 🚀 Instalación

### Opción 1: Usando Docker (Recomendado)

Asegúrate de tener **Docker** y **Docker Compose** instalados en tu sistema.

```bash
# Clonar el repositorio
git clone https://github.com/ikerorozco/Knoledge-Graph-sql/
cd Knowledge-Graph-SQL

# Ejecutar con Docker Compose
docker-compose up --build
```

### Opción 2: Entorno Python Local

```bash
# Clonar el repositorio
git clone https://github.com/ikerorozco/Knoledge-Graph-sql/
cd Knowledge-Graph-SQL

# Crear entorno virtual
python -m venv env

# Activar entorno virtual
source env/bin/activate  # En Linux/Mac
# o
env\Scripts\activate     # En Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Servicios Adicionales

Asegúrate de que **Grobid** esté configurado y ejecutándose antes de iniciar la aplicación principal.

## 💻 Uso

### Ejecución Principal

Para iniciar el proceso de extracción y enriquecimiento de datos desde los PDFs:

```bash
python src/main.py
```

### Aplicación Web Interactiva

Para acceder a la interfaz web de Streamlit:

```bash
streamlit run src/app.py
```

La aplicación estará disponible en `http://localhost:8501`

### Funcionalidades Disponibles

1. **📊 Red Interactiva**: Explora el grafo de conocimiento completo
2. **👥 Autores por Paper**: Analiza la autoría de las publicaciones
3. **🔍 Buscador de Papers**: Busca publicaciones por palabras clave
4. **📅 Línea de Tiempo**: Visualiza proyectos en un diagrama de Gantt
5. **🗺️ Mapa de Organizaciones**: Localiza geográficamente las instituciones

## 📁 Estructura del Proyecto

```
├── 📂 src/
│   ├── 📂 extractors/      # Extracción de datos desde PDFs
│   ├── 📂 api/            # Integración con APIs externas
│   ├── 📂 models/         # Modelos de datos y entidades
│   ├── 📂 graph/          # Construcción del grafo
│   ├── 📂 views/          # Vistas de Streamlit
│   ├── 📄 main.py         # Punto de entrada principal
│   └── 📄 app.py          # Aplicación web
├── 📂 docs/               # Documentación ReadTheDocs
├── 📂 tests/              # Pruebas unitarias
├── 📂 data/               # Datos de entrada
├── 📄 requirements.txt    # Dependencias Python
├── 📄 docker-compose.yml  # Configuración Docker
└── 📄 Dockerfile         # Imagen Docker
```

## 📦 Dependencias

### Principales
- **requests**: Comunicación con APIs externas
- **transformers**: Modelos de lenguaje de Hugging Face
- **sentence-transformers**: Análisis semántico de textos
- **scikit-learn**: Algoritmos de machine learning
- **torch**: Framework de deep learning
- **networkx**: Construcción y análisis de grafos
- **rdflib**: Manejo de datos RDF

### Visualización
- **streamlit**: Framework de aplicaciones web
- **pyvis**: Visualización interactiva de redes
- **matplotlib**: Gráficos estáticos
- **pydeck**: Visualizaciones 3D y mapas
- **altair**: Gráficos declarativos

### Procesamiento de Datos
- **pandas**: Manipulación de datos
- **numpy**: Computación numérica
- **xmltodict**: Procesamiento de XML

### Desarrollo
- **pytest**: Framework de testing
- **black**: Formateador de código
- **flake8**: Linter
- **mypy**: Verificación de tipos

## 📚 Documentación

La documentación completa está disponible en **ReadTheDocs** y se construye usando **Sphinx**.

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo `LICENSE`.

## 👨‍💻 Autores

- **Iker Orozco**
- **Andrea Galindo** 
- **Sergio González**

---

## 🚀 Estado del Proyecto

**Versión**: 1.0.0  
**Estado**: Activo  
**Documentación**: [ReadTheDocs](https://knoledge-graph.readthedocs.io/es/latest/index.html)
