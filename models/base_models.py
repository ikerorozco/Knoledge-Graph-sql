class BaseModel:
    def __init__(self):
        self.flags = {}

    def set_flag(self, name, value):
        self.flags[name] = value

    def get_flag(self, name):
        return self.flags.get(name, False)

    def mostrar_campos_faltantes(self):
        print("\n Campos faltantes:")
        for flag_name, flag_value in self.flags.items():
            if not flag_value:
                print(f"   {flag_name} no encontrado.")

class Proyecto(BaseModel):
    def __init__(self, nombre, financiamiento, rdftype, cordinador, start_date):
        super().__init__()
        self.nombre = nombre
        self.financiamiento = financiamiento
        self.rdftype = rdftype
        self.cordinador = cordinador
        self.start_date = start_date

        self.set_flag('Nombre', nombre is not None)
        self.set_flag('Financiamiento', financiamiento is not None)
        self.set_flag('RdfType', rdftype is not None)
        self.set_flag('Cordinador', cordinador is not None)
        self.set_flag('StartDate', start_date is not None)

    def mostrar_info(self):
        print(" Información del Proyecto:")
        print(f"  Nombre         : {self.nombre}")
        print(f"  Financiamiento : {self.financiamiento or 'No disponible'}")
        print(f"  RDF Type       : {self.rdftype or 'No disponible'}")
        print(f"  Cordinador     : {self.cordinador or 'No disponible'}")
        print(f"  Start Date     : {self.start_date or 'No disponible'}")
        self.mostrar_campos_faltantes()

class Organizacion(BaseModel):
    def __init__(self, nombre, lugar, rdftype, trabajos, links):
        super().__init__()
        self.nombre = nombre
        self.lugar = lugar
        self.rdftype = rdftype
        self.trabajos = trabajos
        self.links = links

        self.set_flag('Nombre', nombre is not None)
        self.set_flag('Lugar', lugar is not None)
        self.set_flag('RdfType', rdftype is not None)
        self.set_flag('Trabajos', trabajos is not None)
        self.set_flag('Links', links is not None)

    def mostrar_info(self):
        print(" Información de la Organización:")
        print(f"  Nombre         : {self.nombre}")
        print(f"  Lugar          : {self.lugar or 'No disponible'}")
        print(f"  RDF Type       : {self.rdftype or 'No disponible'}")
        print(f"  Trabajos       : {self.trabajos or 'No disponible'}")
        print(f"  Links          : {self.links or 'No disponible'}")
        self.mostrar_campos_faltantes()

class Author(BaseModel):
    def __init__(self, nombre, rdf_type=None, profesion=None, trabajos=None):
        super().__init__()
        self.nombre = nombre
        self.rdf_type = rdf_type
        self.profesion = profesion
        self.trabajos = trabajos

        self.set_flag('Nombre', nombre is not None)
        self.set_flag('RdfType', rdf_type is not None)
        self.set_flag('Profesion', profesion is not None)
        self.set_flag('Trabajos', trabajos is not None)

    def mostrar_info(self):
        print(" Información del Autor:")
        print(f"  Nombre         : {self.nombre}")
        print(f"  RDF Type       : {self.rdf_type or 'No disponible'}")
        print(f"  Profesión      : {self.profesion or 'No disponible'}")
        print(f"  Trabajos       : {self.trabajos or 'No disponible'}")
        self.mostrar_campos_faltantes()

class Paper(BaseModel):
    def __init__(self, title, doi, date, idioma, veces_citado, paginas, rdf_type, autores=None):
        super().__init__()
        self.title = title
        self.doi = doi
        self.date = date
        self.idioma = idioma
        self.veces_citado = veces_citado
        self.paginas = paginas
        self.rdf_type = rdf_type
        self.autores = autores or []

        self.set_flag('Title', title is not None)
        self.set_flag('Doi', doi is not None)
        self.set_flag('Date', date is not None)
        self.set_flag('Idioma', idioma is not None)
        self.set_flag('VecesCitado', veces_citado is not None)
        self.set_flag('Paginas', paginas is not None)
        self.set_flag('RdfType', rdf_type is not None)

    def mostrar_info(self):
        print(" Información del Paper:")
        print(f"  Título         : {self.title}")
        print(f"  DOI            : {self.doi}")
        print(f"  Fecha          : {self.date}")
        print(f"  Idioma         : {self.idioma}")
        print(f"  Veces citado   : {self.veces_citado}")
        print(f"  Páginas        : {self.paginas}")
        print(f"  RDF Type       : {self.rdf_type}")
        self.mostrar_campos_faltantes()

        if self.autores:
            print("\n Autores:")
            for autor in self.autores:
                autor.mostrar_info()
                print("\n") 