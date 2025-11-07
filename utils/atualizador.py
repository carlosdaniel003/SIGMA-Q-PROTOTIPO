import os
import pandas as pd
import streamlit as st

import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_PATH = os.path.join(BASE_DIR, "data", "quality_control_outubro.xlsx")

def carregar_base(path: str = None, usecols: list | None = None) -> pd.DataFrame:
    """
    Carrega a base oficial de dados de forma segura.
    """

    caminho = path or DEFAULT_PATH
    st.write(f"📂 Caminho da base: {caminho}")

    if not os.path.exists(caminho):
        st.error(f"❌ Arquivo não encontrado: {caminho}")
        st.stop()

    try:
        df = pd.read_excel(caminho, usecols=usecols)
        df.columns = (
            df.columns.str.strip()
            .str.upper()
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("ascii")
            .str.replace(" ", "_")
        )
        df = df.dropna(how="all").reset_index(drop=True)
        st.success(f"✅ Base carregada com sucesso ({len(df)} registros, {len(df.columns)} colunas).")
        return df

    except Exception as e:
        st.error(f"⚠️ Erro ao carregar base: {e}")
        st.stop()

    st.write(f"📂 Usando base em: `{caminho}`")

    # Carrega planilha
    df = pd.read_excel(caminho, usecols=usecols)
    df.columns = (
        df.columns.str.strip()
        .str.upper()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("ascii")
        .str.replace(" ", "_")
    )
    df = df.dropna(how="all").reset_index(drop=True)
    st.success(f"✅ Base carregada com sucesso: {len(df)} registros, {len(df.columns)} colunas.")
    return df
