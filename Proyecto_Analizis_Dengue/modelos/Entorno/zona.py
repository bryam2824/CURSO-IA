from dataclasses import dataclass, field


@dataclass
class Zona:

    # Ubicación administrativa
    departamento: str = None
    municipio: str = None

    # Coordenadas
    latitud: float = None
    longitud: float = None

    # Datos manuales validados
    datos_adicionales: dict = field(default_factory=dict)

def agregar_dato(
    self,
    nombre,
    valor
):
    self.datos_adicionales[nombre] = valor