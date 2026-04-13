# 💊 MediCuidar — Controle de Medicamentos para Idosos

> **🌐 Aplicação publicada:** [https://controle-medicamentos-idosos-inqqzrveyrx6qxnmzbwxhu.streamlit.app/]

Sistema web para auxiliar cuidadores no controle de medicamentos
e horários de idosos, com cadastro de endereço automático via CEP.

## ✨ Funcionalidades

- 👤 Cadastro de pacientes com endereço auto-preenchido pelo CEP (via ViaCEP)
- 💊 Registro de medicamentos com doses e horários
- 📋 Listagem completa de pacientes e suas medicações

## 🔌 API Integrada

| API | Finalidade |
|-----|-----------|
| [ViaCEP](https://viacep.com.br/) | Busca endereço completo a partir do CEP |

## 🚀 Como executar localmente

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/controle-medicamentos-idosos.git
cd controle-medicamentos-idosos

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
streamlit run app/main.py
```

## 🧪 Executar os testes

```bash
pytest tests/ -v
```

## 🛠️ Tecnologias

- Python 3.11
- Streamlit
- Requests
- Pytest
- GitHub Actions (CI)
- Streamlit Community Cloud (Deploy)