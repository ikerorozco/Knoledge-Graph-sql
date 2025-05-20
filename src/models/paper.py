from typing import Optional, List
from .author import Author
from .organization import Organization


class Paper:
    """Modelo que representa un paper académico."""
    
    def __init__(self, title: str, doi: Optional[str] = None, date: Optional[str] = None,
                 idioma: Optional[str] = None, veces_citado: Optional[int] = None,
                 paginas: Optional[int] = None, rdf_type: Optional[str] = None,
                 autores: Optional[List[Author]] = None, organization: Optional[List[Organization]] = None):
        """
        Inicializa un paper con sus atributos.
        
        Args:
            title (str): Título del paper
            doi (Optional[str], optional): DOI del paper. Defaults to None.
            date (Optional[str], optional): Fecha de publicación. Defaults to None.
            idioma (Optional[str], optional): Idioma del paper. Defaults to None.
            veces_citado (Optional[int], optional): Número de citas. Defaults to None.
            paginas (Optional[int], optional): Número de páginas. Defaults to None.
            rdf_type (Optional[str], optional): Tipo RDF del paper. Defaults to None.
            autores (Optional[List[Author]], optional): Lista de autores. Defaults to None.
            organization (Optional[List[Organization]], optional): Lista de organizaciones. Defaults to None.
        """
        self.title = title
        self.doi = doi
        self.date = date
        self.idioma = idioma
        self.veces_citado = veces_citado
        self.paginas = paginas
        self.rdf_type = rdf_type
        self.autores = autores if autores is not None else []
        self.organization = organization if organization is not None else []
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