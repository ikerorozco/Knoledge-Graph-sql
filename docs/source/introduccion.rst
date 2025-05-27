============
Introducción
============


🔬 Metodología y Enfoque
========================

Flujo de Trabajo Principal
--------------------------

.. mermaid::

   graph TD
       A[Documentos PDF] --> B[Extracción con Grobid]
       B --> C[Metadatos Básicos]
       C --> D[Enriquecimiento OpenAIRE/OpenAlex]
       D --> E[Datos Enriquecidos]
       E --> F[Análisis Semántico HuggingFace]
       F --> G[Similitudes Temáticas]
       G --> H[Construcción del Grafo]
       H --> I[Visualización Interactiva]

1. **Extracción de Información**
   
   * Utiliza **Grobid** para extraer metadatos estructurados
   * Identifica títulos, autores, abstracts y referencias
   * Procesa documentos de manera automática y escalable

2. **Enriquecimiento de Datos**
   
   * Consulta **OpenAIRE** para información de proyectos europeos
   * Integra datos de **OpenAlex** para métricas y afiliaciones
   * Vincula entidades mediante identificadores únicos (DOI, ORCID)

3. **Análisis Semántico**
   
   * Utiliza modelos de **Sentence Transformers** para embeddings
   * Calcula similitudes semánticas entre abstracts
   * Identifica clusters temáticos automáticamente

4. **Construcción del Grafo**
   
   * Crea nodos para papers, autores, instituciones y proyectos
   * Establece relaciones basadas en coautoría y similitud semántica
   * Estructura el grafo para consultas eficientes

🧠 Fundamentos Teóricos
=======================

Grafos de Conocimiento
-----------------------

Un **grafo de conocimiento** es una representación estructurada del conocimiento que utiliza:

* **Nodos**: Entidades (papers, autores, instituciones)
* **Aristas**: Relaciones entre entidades
* **Propiedades**: Atributos de nodos y relaciones


Análisis de Texto Semántico
----------------------------

La aplicación emplea técnicas de NLP:

* **Embeddings de Oraciones**: Representación vectorial de abstracts
* **Similitud Coseno**: Medida de proximidad semántica
* **Clustering**: Agrupación automática de documentos similares


🌟 Casos de Uso Principales
===========================

Para Investigadores
-------------------

* **Descubrimiento de Literatura**: Encuentra papers relacionados automáticamente
* **Análisis de Colaboraciones**: Visualiza redes de coautoría
* **Identificación de Tendencias**: Detecta temas emergentes en el campo
* **Mapeo de Influencia**: Analiza el impacto de publicaciones

Para Bibliotecarios
--------------------

* **Catalogación Inteligente**: Organiza colecciones automáticamente
* **Recomendaciones**: Sugiere lecturas relacionadas
* **Análisis de Colecciones**: Evalúa cobertura temática
* **Gestión de Metadatos**: Enriquece registros bibliográficos

Para Administradores de Investigación
--------------------------------------

* **Evaluación de Impacto**: Mide la influencia de investigaciones
* **Identificación de Expertos**: Localiza especialistas en temas específicos
* **Análisis de Colaboraciones**: Evalúa redes de investigación
* **Planificación Estratégica**: Identifica oportunidades de investigación

🔧 Tecnologías
====================

Procesamiento de Documentos
----------------------------

* **Grobid**: Motor de extracción de metadatos de PDFs científicos
* **XMLtoDict**: Procesamiento de respuestas XML estructuradas
* **Requests**: Comunicación con APIs REST

Análisis Semántico
-------------------

* **Hugging Face Transformers**: Modelos de lenguaje preentrenados
* **Sentence Transformers**: Embeddings especializados para oraciones
* **Scikit-learn**: Algoritmos de clustering y similitud

Construcción de Grafos
-----------------------

* **NetworkX**: Construcción y análisis de grafos
* **RDFLib**: Exportación a formatos semánticos estándar
* **Neo4j** (opcional): Base de datos de grafos para escalabilidad

Visualización
-------------

* **Streamlit**: Framework de aplicaciones web interactivas
* **PyVis**: Visualización interactiva de redes
* **Matplotlib/Altair**: Gráficos estadísticos y analíticos
