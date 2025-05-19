from typing import Optional, List
from .author import Author
from .organization import Organization


class Paper:
    """Modelo que representa un paper académico."""
    
    def __init__(self, title: str, doi: Optional[str], date: Optional[str],
                 idioma: Optional[str], veces_citado: Optional[int],
                 paginas: Optional[int], rdf_type: Optional[str],
                 autores: List[Author],organization: List[Organization]):
        """
        Inicializa un paper con sus atributos.
        
        Args:
            title (str): Título del paper
            doi (Optional[str]): DOI del paper
            date (Optional[str]): Fecha de publicación
            idioma (Optional[str]): Idioma del paper
            veces_citado (Optional[int]): Número de citas
            paginas (Optional[int]): Número de páginas
            rdf_type (Optional[str]): Tipo RDF del paper
            autores (List[Author]): Lista de autores
        """
        self.title = title
        self.doi = doi
        self.date = date
        self.idioma = idioma
        self.veces_citado = veces_citado
        self.paginas = paginas
        self.rdf_type = rdf_type
        self.autores = autores
        self.organization = organization
        self.flags = {}

        self.set_flag('Title', title is not None)
        self.set_flag('Doi', doi is not None)
        self.set_flag('Date', date is not None)
        self.set_flag('Idioma', idioma is not None)
        self.set_flag('VecesCitado', veces_citado is not None)
        self.set_flag('Paginas', paginas is not None)
        self.set_flag('RdfType', rdf_type is not None)

    def set_flag(self, nombre: str, valor: bool) -> None:
        """
        Establece un flag para un campo específico.
        
        Args:
            nombre (str): Nombre del campo
            valor (bool): Estado del campo (True si está presente, False si falta)
        """
        self.flags[nombre] = valor

    def mostrar_info(self) -> None:
        """Muestra la información del paper y sus autores."""
        print(" Información del Paper:")
        print(f"  Título         : {self.title}")
        print(f"  DOI            : {self.doi}")
        print(f"  Fecha          : {self.date}")
        print(f"  Idioma         : {self.idioma}")
        print(f"  Veces citado   : {self.veces_citado}")
        print(f"  Páginas        : {self.paginas}")
        print(f"  RDF Type       : {self.rdf_type}")
        print("\n")

        print(" Autores:")
        for autor in self.autores:
            autor.mostrar_info()
            print("\n") 
        print(" Organizaciones:")
        for org in self.organization:
            org.mostrar_info()
            print("\n")