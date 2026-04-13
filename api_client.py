import requests


VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"


def buscar_endereco_por_cep(cep: str) -> dict:
    """
    Consulta a API ViaCEP e retorna os dados de endereço.
    Lança ValueError se o CEP for inválido ou não encontrado.
    """
    cep_limpo = cep.replace("-", "").replace(".", "").strip()

    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        raise ValueError(f"CEP inválido: '{cep}'. Informe 8 dígitos numéricos.")

    url = VIACEP_URL.format(cep=cep_limpo)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise ConnectionError("Tempo de resposta esgotado ao consultar o ViaCEP.")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Falha na conexão com ViaCEP: {e}")

    dados = response.json()

    if "erro" in dados:
        raise ValueError(f"CEP '{cep}' não encontrado na base dos Correios.")

    return {
        "cep": dados.get("cep", cep_limpo),
        "logradouro": dados.get("logradouro", ""),
        "bairro": dados.get("bairro", ""),
        "cidade": dados.get("localidade", ""),
        "estado": dados.get("uf", ""),
    }