# ============================================
# utils/model_manager.py
# ============================================
# Gerencia o carregamento e salvamento do modelo
# e do vetorizador TF-IDF para o SIGMA-Q.
# ============================================

import os
import joblib
import streamlit as st

# Caminhos padrão
MODELO_PATH = "model/modelo_classificacao.pkl"
VETORIZADOR_PATH = "model/vectorizer.pkl"

def carregar_modelos():
    """
    Carrega o modelo de classificação e o vetorizador TF-IDF do disco.
    Retorna (modelo, vetorizador).
    """
    try:
        if not os.path.exists(MODELO_PATH):
            st.sidebar.error(f"❌ Modelo não encontrado em {MODELO_PATH}")
            return None, None

        if not os.path.exists(VETORIZADOR_PATH):
            st.sidebar.error(f"❌ Vetorizador não encontrado em {VETORIZADOR_PATH}")
            return None, None

        modelo = joblib.load(MODELO_PATH)
        vetorizador = joblib.load(VETORIZADOR_PATH)
        st.sidebar.success("✅ Modelo e vetorizador carregados com sucesso!")
        return modelo, vetorizador

    except Exception as e:
        st.sidebar.error(f"⚠️ Erro ao carregar modelos: {e}")
        return None, None


def salvar_modelos(modelo, vetorizador):
    """
    Salva o modelo e o vetorizador atualizados no disco.
    """
    try:
        os.makedirs("model", exist_ok=True)
        joblib.dump(modelo, MODELO_PATH)
        joblib.dump(vetorizador, VETORIZADOR_PATH)
        st.success("💾 Modelos salvos com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro ao salvar modelos: {e}")


def verificar_modelos():
    """
    Verifica se os arquivos de modelo e vetorizador estão disponíveis.
    Retorna True se ambos existirem.
    """
    modelo_existe = os.path.exists(MODELO_PATH)
    vetor_existe = os.path.exists(VETORIZADOR_PATH)

    if modelo_existe and vetor_existe:
        st.sidebar.info("🧠 Modelos prontos para uso.")
        return True
    else:
        st.sidebar.warning("⚠️ Modelos ausentes ou incompletos.")
        return False
