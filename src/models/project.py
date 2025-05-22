from typing import Optional
from datetime import date

from models.paper import Paper


class Project:
    """Modelo que representa un proyecto."""
    
    def __init__(self, nombre: str, fundedAmount: Optional[float] = None,
                 startdate: Optional[date] = None, enddate: Optional[date] = None, papers: Optional[list] = None):
        """
        Inicializa un proyecto con sus atributos.
        
        Args:
            nombre (str): Nombre del proyecto
            fundedAmount (Optional[float], optional): Cantidad de dinero invertido en el proyecto. Defaults to None.
            startdate (Optional[date], optional): Fecha de inicio del proyecto. Defaults to None.
            enddate (Optional[date], optional): Fecha de finalización del proyecto. Defaults to None.
            papers (Optional[list], optional): Lista de papers asociados al proyecto. Defaults to None.
        """
        self.nombre = nombre
        self.fundedAmount = fundedAmount
        self.startdate = startdate
        self.enddate = enddate
        self.flags = {}
        self.papers = papers
        self.set_flag('Nombre', nombre is not None)
        self.set_flag('FundedAmount', fundedAmount is not None)
        self.set_flag('StartDate', startdate is not None)
        self.set_flag('EndDate', enddate is not None)

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
        """Muestra la información del proyecto."""
        print(" Información del Proyecto:")
        print(f"  Nombre         : {self.nombre}")
        print(f"  Cantidad Invertida    : {self.fundedAmount or 'No disponible'}")
        print(f"  Fecha Inicio   : {self.startdate or 'No disponible'}")
        print(f"  Fecha Fin   : {self.enddate or 'No disponible'}")
        print(f"  Papers asociados: {self.papers or 'No hay papers asociados'}")

    def agregar_paper(self, paper: Paper) -> None:
        """Agrega un paper a la lista de papers asociados al proyecto."""
        if self.papers is None:
            self.papers = []
        self.papers.append(paper)