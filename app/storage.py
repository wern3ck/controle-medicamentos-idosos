import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from api_client import buscar_endereco_por_cep
from models import Paciente, Endereco, Medicamento
from storage import carregar_pacientes, salvar_pacientes


ARQUIVO = "dados_pacientes.json"


def _paciente_para_dict(p: Paciente) -> dict:
    return {
        "nome": p.nome,
        "idade": p.idade,
        "endereco": {
            "cep": p.endereco.cep,
            "logradouro": p.endereco.logradouro,
            "bairro": p.endereco.bairro,
            "cidade": p.endereco.cidade,
            "estado": p.endereco.estado,
        },
        "medicamentos": [
            {"nome": m.nome, "dose": m.dose, "horarios": m.horarios}
            for m in p.medicamentos
        ],
    }


def _dict_para_paciente(d: dict) -> Paciente:
    end = Endereco(**d["endereco"])
    meds = [Medicamento(**m) for m in d.get("medicamentos", [])]
    return Paciente(nome=d["nome"], idade=d["idade"], endereco=end, medicamentos=meds)


def carregar_pacientes() -> List[Paciente]:
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return [_dict_para_paciente(d) for d in json.load(f)]


def salvar_pacientes(pacientes: List[Paciente]) -> None:
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump([_paciente_para_dict(p) for p in pacientes], f, ensure_ascii=False, indent=2)