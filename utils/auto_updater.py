import os
import time
import streamlit as st
import pandas as pd

def verificar_atualizacao(caminho_base, ultima_modificacao):
    """Verifica se o arquivo foi modificado."""
    if os.path.exists(caminho_base):
        nova_modificacao = os.path.getmtime(caminho_base)
        if nova_modificacao != ultima_modificacao:
            st.toast("📂 Nova base detectada! Recarregando dados...")
            return True, nova_modificacao
    return False, ultima_modificacao
