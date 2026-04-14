"""
Testes de Integração — valida comunicação com a API ViaCEP.
"""
import pytest
from unittest.mock import patch, MagicMock
from api_client import buscar_endereco_por_cep


# ── Teste REAL (chama a API de verdade) ────────────────────────────
class TestIntegracaoViaCEPReal:
    """
    Teste real: requer conexão com a internet.
    Valida que a API responde e retorna campos esperados.
    """

    def test_cep_valido_retorna_dados_corretos(self):
        resultado = buscar_endereco_por_cep("01310-100")  # Avenida Paulista
        assert resultado["cidade"] == "São Paulo"
        assert resultado["estado"] == "SP"
        assert resultado["logradouro"] != ""
        assert resultado["cep"] == "01310-100"

    def test_cep_sem_hifen_tambem_funciona(self):
        resultado = buscar_endereco_por_cep("01310100")
        assert resultado["cidade"] == "São Paulo"


# ── Testes com MOCK (não dependem de internet) ────────────────────
class TestIntegracaoViaCEPMock:
    """
    Testes mockados: simulam a resposta da API sem precisar de rede.
    Rodam em qualquer ambiente, incluindo o CI/CD.
    """

    def test_retorna_endereco_formatado_corretamente(self):
        resposta_simulada = MagicMock()
        resposta_simulada.json.return_value = {
            "cep": "01310-100",
            "logradouro": "Avenida Paulista",
            "bairro": "Bela Vista",
            "localidade": "São Paulo",
            "uf": "SP",
        }
        resposta_simulada.raise_for_status = MagicMock()

        with patch("app.api_client.requests.get", return_value=resposta_simulada):
            resultado = buscar_endereco_por_cep("01310100")

        assert resultado["logradouro"] == "Avenida Paulista"
        assert resultado["bairro"] == "Bela Vista"
        assert resultado["cidade"] == "São Paulo"
        assert resultado["estado"] == "SP"

    def test_cep_inexistente_levanta_value_error(self):
        resposta_simulada = MagicMock()
        resposta_simulada.json.return_value = {"erro": True}
        resposta_simulada.raise_for_status = MagicMock()

        with patch("app.api_client.requests.get", return_value=resposta_simulada):
            with pytest.raises(ValueError, match="não encontrado"):
                buscar_endereco_por_cep("00000000")

    def test_cep_com_menos_de_8_digitos_levanta_value_error(self):
        with pytest.raises(ValueError, match="inválido"):
            buscar_endereco_por_cep("1234")

    def test_cep_com_letras_levanta_value_error(self):
        with pytest.raises(ValueError, match="inválido"):
            buscar_endereco_por_cep("ABCDEFGH")

    def test_timeout_levanta_connection_error(self):
        import requests as req
        with patch("app.api_client.requests.get", side_effect=req.exceptions.Timeout):
            with pytest.raises(ConnectionError, match="esgotado"):
                buscar_endereco_por_cep("01310100")