from dataclasses import dataclass, asdict

@dataclass
class Oferta:
    titulo: str
    empresa: str
    ciudad: str
    enlace: str
    salario: str = "N/A"
    contrato: str = "N/A"
    jornada: str = "N/A"
    experiencia: str = "N/A"

    def a_diccionario(self):
        # convertimos la oferta a dict para exportar a csv o json
        return asdict(self)