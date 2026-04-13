import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from api_client import buscar_endereco_por_cep
from models import Paciente, Endereco, Medicamento
from storage import carregar_pacientes, salvar_pacientes

st.set_page_config(page_title="💊 MediCuidar", page_icon="💊", layout="centered")

st.title("💊 MediCuidar")
st.caption("Controle de medicamentos e horários para idosos")

# ── Sidebar: navegação ──────────────────────────────────────────────
pagina = st.sidebar.radio(
    "Menu",
    ["📋 Pacientes", "➕ Cadastrar Paciente", "💉 Adicionar Medicamento"],
)

pacientes = carregar_pacientes()

# ──────────────────────────────────────────────────────────────────
# PÁGINA: Listar pacientes
# ──────────────────────────────────────────────────────────────────
if pagina == "📋 Pacientes":
    st.header("Pacientes Cadastrados")

    if not pacientes:
        st.info("Nenhum paciente cadastrado ainda. Use o menu lateral para adicionar.")
    else:
        for i, p in enumerate(pacientes):
            with st.expander(f"👤 {p.nome} — {p.idade} anos"):
                st.write(f"📍 **Endereço:** {p.endereco.logradouro}, {p.endereco.bairro} — {p.endereco.cidade}/{p.endereco.estado} (CEP: {p.endereco.cep})")
                if p.medicamentos:
                    st.write("**Medicamentos:**")
                    for m in p.medicamentos:
                        horarios = ", ".join(m.horarios)
                        st.write(f"  • 💊 **{m.nome}** — {m.dose} — Horários: {horarios}")
                else:
                    st.write("_Nenhum medicamento cadastrado._")

# ──────────────────────────────────────────────────────────────────
# PÁGINA: Cadastrar paciente
# ──────────────────────────────────────────────────────────────────
elif pagina == "➕ Cadastrar Paciente":
    st.header("Cadastrar Novo Paciente")

    nome = st.text_input("Nome completo")
    idade = st.number_input("Idade", min_value=1, max_value=120, value=70)
    cep = st.text_input("CEP (somente números)", placeholder="01310100")

    endereco_info = None

    if st.button("🔍 Buscar endereço pelo CEP"):
        if not cep:
            st.warning("Informe o CEP antes de buscar.")
        else:
            with st.spinner("Consultando ViaCEP..."):
                try:
                    endereco_info = buscar_endereco_por_cep(cep)
                    st.session_state["endereco"] = endereco_info
                    st.success("Endereço encontrado!")
                except (ValueError, ConnectionError) as e:
                    st.error(str(e))

    # Exibe endereço encontrado
    if "endereco" in st.session_state:
        e = st.session_state["endereco"]
        st.write(f"📍 {e['logradouro']}, {e['bairro']} — {e['cidade']}/{e['estado']}")

    if st.button("💾 Salvar Paciente"):
        if not nome:
            st.warning("Informe o nome do paciente.")
        elif "endereco" not in st.session_state:
            st.warning("Busque o CEP antes de salvar.")
        else:
            e = st.session_state["endereco"]
            novo = Paciente(
                nome=nome,
                idade=int(idade),
                endereco=Endereco(**e),
            )
            pacientes.append(novo)
            salvar_pacientes(pacientes)
            del st.session_state["endereco"]
            st.success(f"✅ Paciente **{nome}** cadastrado com sucesso!")
            st.balloons()

# ──────────────────────────────────────────────────────────────────
# PÁGINA: Adicionar medicamento
# ──────────────────────────────────────────────────────────────────
elif pagina == "💉 Adicionar Medicamento":
    st.header("Adicionar Medicamento")

    if not pacientes:
        st.info("Cadastre um paciente primeiro.")
    else:
        nomes = [p.nome for p in pacientes]
        escolhido = st.selectbox("Selecione o paciente", nomes)

        nome_med = st.text_input("Nome do medicamento", placeholder="Ex: Losartana")
        dose = st.text_input("Dose", placeholder="Ex: 50mg — 1 comprimido")
        horarios_raw = st.text_input(
            "Horários (separados por vírgula)", placeholder="Ex: 08:00, 20:00"
        )

        if st.button("➕ Adicionar"):
            if not nome_med or not dose or not horarios_raw:
                st.warning("Preencha todos os campos.")
            else:
                horarios = [h.strip() for h in horarios_raw.split(",") if h.strip()]
                idx = nomes.index(escolhido)
                pacientes[idx].medicamentos.append(
                    Medicamento(nome=nome_med, dose=dose, horarios=horarios)
                )
                salvar_pacientes(pacientes)
                st.success(f"✅ Medicamento **{nome_med}** adicionado para {escolhido}!")