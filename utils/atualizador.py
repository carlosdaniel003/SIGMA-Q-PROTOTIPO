import os
import pandas as pd
import streamlit as st

def carregar_base(path: str = None, usecols: list | None = None) -> pd.DataFrame:
    """
    Carrega a base oficial de dados de forma segura.
    Detecta ambiente local ou Streamlit Cloud automaticamente.
    """

    # Caminhos possíveis
    local_path = os.path.join("data", "quality_control_outubro.xlsx")
    cloud_path = os.path.join("/mount/src/sigma-q-prototipo/data", "quality_control_outubro.xlsx")

    # Escolhe o que existir
    if os.path.exists(local_path):
        caminho = local_path
    elif os.path.exists(cloud_path):
        caminho = cloud_path
    else:
        st.error("❌ Base de dados não encontrada em nenhum caminho esperado.")
        st.info("Verifique se o arquivo está incluído no GitHub ou se o nome está correto.")
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
