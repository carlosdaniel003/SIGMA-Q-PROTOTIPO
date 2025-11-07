# utils/atualizador.py
import pandas as pd
import os
import streamlit as st

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_PATH = os.path.join(BASE_DIR, "data", "quality_control_outubro.xlsx")

def carregar_base(path: str = None, usecols: list | None = None) -> pd.DataFrame:
    """
    Carrega a base de dados oficial (oculta) de forma segura.
    Mostra mensagens amigáveis caso o arquivo não exista no ambiente.
    """

    caminho = path or DEFAULT_PATH
    st.write(f"📂 Caminho de busca da base: `{caminho}`")

    # Se o arquivo não existir, tenta exibir aviso e seguir sem travar
    if not os.path.exists(caminho):
        st.warning("⚠️ A base de dados oficial não foi encontrada no ambiente atual.")
        st.info("""
        Possíveis causas:
        - O arquivo `quality_control_outubro.xlsx` não foi incluído no repositório GitHub.
        - A pasta `data/` está vazia no Streamlit Cloud.
        - O caminho padrão não foi atualizado.
        """)
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

        # Remove linhas totalmente vazias
        df = df.dropna(how="all").reset_index(drop=True)

        st.success(f"✅ Base carregada com sucesso: {len(df)} registros, {len(df.columns)} colunas.")
        return df

    except Exception as e:
        st.error(f"❌ Erro ao ler a planilha: {e}")
        st.stop()
