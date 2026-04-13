from dataclasses import dataclass, field
from typing import List


@dataclass
class Endereco:
    cep: str
    logradouro: str
    bairro: str
    cidade: str
    estado: str


@dataclass
class Medicamento:
    nome: str
    dose: str
    horarios: List[str]  # Ex: ["08:00", "20:00"]


@dataclass
class Paciente:
    nome: str
    idade: int
    endereco: Endereco
    medicamentos: List[Medicamento] = field(default_factory=list)