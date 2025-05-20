from typing import Optional, List

class Organization:
    """Modelo que representa una organización académica."""
    
    def __init__(self, nombre: str, lugar: Optional[str] = None, rdftype: Optional[str] = None,
                 trabajos: Optional[int] = None, links: Optional[List[str]] = None):
        """
        Inicializa una organización con sus atributos.
        
        Args:
            nombre (str): Nombre de la organización
            lugar (Optional[str], optional): Ubicación de la organización. Defaults to None.
            rdftype (Optional[str], optional): Tipo RDF de la organización. Defaults to None.
            trabajos (Optional[int], optional): Número de trabajos asociados. Defaults to None.
            links (Optional[List[str]], optional): Lista de enlaces relacionados. Defaults to None.
        """
        self.nombre = nombre
        self.lugar = lugar
        self.rdftype = rdftype
        self.trabajos = trabajos
        self.links = links if links is not None else []
        self.flags = {}

        self.set_flag('Nombre', nombre is not None)
        self.set_flag('Lugar', lugar is not None)
        self.set_flag('RdfType', rdftype is not None)
        self.set_flag('Trabajos', trabajos is not None)
        self.set_flag('Links', links is not None)

    def set_flag(self, nombre: str, valor: bool) -> None:
        """
        Establece un flag para un campo específico.
        
        Args:
            nombre (str): Nombre del campo
            valor (bool): Estado del campo (True si está presente, False si falta)
        """
        self.flags[nombre] = valor

    def mostrar_campos_faltantes(self) -> None:
        """Muestra los campos que no están presentes en el modelo."""
        print("\n Campos faltantes:")
        for nombre, valor in self.flags.items():
            if not valor:
                print(f"   {nombre} no encontrado.")

    def mostrar_info(self) -> None:
        """Muestra la información de la organización."""
        print(" Información de la Organización:")
        print(f"  Nombre         : {self.nombre}")
        print(f"  Lugar          : {self.lugar or 'No disponible'}")
        print(f"  RDF Type       : {self.rdftype or 'No disponible'}")
        print(f"  Trabajos       : {self.trabajos or 'No disponible'}")
        print(f"  Links          : {self.links or 'No disponible'}")
        self.mostrar_campos_faltantes() 