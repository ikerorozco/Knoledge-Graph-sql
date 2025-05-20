from typing import Optional, List

class Author:
    """Modelo que representa a un autor de papers académicos."""
    
    def __init__(self, nombre: str, rdf_type: Optional[str] = None, 
                 profesion: Optional[str] = None, trabajos: Optional[int] = None):
        """
        Inicializa un autor con sus atributos.
        
        Args:
            nombre (str): Nombre del autor
            rdf_type (Optional[str], optional): Tipo RDF del autor. Defaults to None.
            profesion (Optional[str], optional): Profesión del autor. Defaults to None.
            trabajos (Optional[int], optional): Número de trabajos del autor. Defaults to None.
        """
        self.nombre = nombre
        self.rdf_type = rdf_type
        self.profesion = profesion
        self.trabajos = trabajos
        self.flags = {}

        self.set_flag('Nombre', nombre is not None)
        self.set_flag('RdfType', rdf_type is not None)
        self.set_flag('Profesion', profesion is not None)
        self.set_flag('Trabajos', trabajos is not None)

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
        """Muestra la información del autor."""
        print(" Información del Autor:")
        print(f"  Nombre         : {self.nombre}")
        print(f"  RDF Type       : {self.rdf_type or 'No disponible'}")
        print(f"  Profesión      : {self.profesion or 'No disponible'}")
        print(f"  Trabajos       : {self.trabajos or 'No disponible'}")
