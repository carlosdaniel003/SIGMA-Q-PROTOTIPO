# ============================================
# utils/atualizador.py
# ============================================
# Funções para monitorar e atualizar automaticamente
# a base de dados do SIGMA-Q quando for alterada.
# ============================================

import os
import time
import pandas as pd
import streamlit as st

# Caminho padrão da base
BASE_PATH = "data/base_de_dados.xlsx"

def carregar_base(caminho_base=BASE_PATH):
    """
    Carrega o arquivo Excel da base de dados local.
    Retorna um DataFrame do pandas.
    """
    try:
        df = pd.read_excel(caminho_base, engine="openpyxl")
        st.success(f"✅ Base carregada: {caminho_base}")
        st.info(f"📊 Total de linhas: {len(df)}")
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar base: {e}")
        return pd.DataFrame()

def monitorar_base(caminho_base=BASE_PATH, intervalo=10):
    """
    Monitora alterações no arquivo Excel e retorna True
    se houver modificação desde a última execução.
    """
    if not os.path.exists(caminho_base):
        st.error(f"⚠️ Arquivo não encontrado: {caminho_base}")
        return False

    # Usar estado persistente do Streamlit
    if "ultimo_modificado" not in st.session_state:
        st.session_state.ultimo_modificado = os.path.getmtime(caminho_base)
        return False

    novo_modificado = os.path.getmtime(caminho_base)
    if novo_modificado != st.session_state.ultimo_modificado:
        st.session_state.ultimo_modificado = novo_modificado
        st.toast("📂 Nova versão da base detectada! Recarregando dados...")
        return True

    return False

