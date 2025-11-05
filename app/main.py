import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# =========================
# CONFIGURAÇÃO INICIAL
# =========================
st.set_page_config(page_title="SIGMA-Q - Dashboard de Defeitos", layout="wide")

st.title("📊 SIGMA-Q - Dashboard de Defeitos na Linha de Montagem")
st.markdown("Monitoramento inteligente e classificação automática de defeitos")

# =========================
# CARREGAR MODELO E VETORIZADOR
# =========================
modelo_path = "model/modelo_classificacao.pkl"
vetorizador_path = "model/vectorizer.pkl"

if os.path.exists(modelo_path) and os.path.exists(vetorizador_path):
    modelo = joblib.load(modelo_path)
    vetorizador = joblib.load(vetorizador_path)
    st.sidebar.success("✅ Modelo carregado com sucesso!")
else:
    st.sidebar.error("❌ Modelo não encontrado! Execute o script de treino primeiro.")
    st.stop()

# =========================
# UPLOAD / LEITURA DOS DADOS
# =========================
st.header("📂 Carregar Base de Dados")
arquivo = st.file_uploader("Selecione um arquivo Excel (.xlsx)", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)
else:
    base_padrao = os.path.join("data", "base_de_dados.xlsx")
    if os.path.exists(base_padrao):
        try:
            df = pd.read_excel(base_padrao, engine="openpyxl")
            st.info(f"Usando base padrão existente: {base_padrao}")
        except Exception as e:
            st.error(f"❌ Erro ao abrir a base de dados: {e}")
            st.stop()
    else:
        st.warning("⚠️ Arquivo 'base_de_dados.xlsx' não encontrado na pasta /data.")
        st.stop()

    else:
        st.warning("Envie um arquivo .xlsx para continuar.")
        st.stop()

st.write("### Visualização da Base de Dados:")
st.dataframe(df.head(), use_container_width=True)

# =========================
# CLASSIFICAÇÃO AUTOMÁTICA
# =========================
st.header("🤖 Classificação Automática")

if "DESCRIÇÃO DA FALHA" in df.columns:
    descricoes = df["DESCRIÇÃO DA FALHA"].astype(str)
    X_tfidf = vetorizador.transform(descricoes)
    predicoes = modelo.predict(X_tfidf)
    df["CATEGORIA_PREDITA"] = predicoes

    st.success("✅ Classificação concluída!")
    st.dataframe(df[["DESCRIÇÃO DA FALHA", "CATEGORIA_PREDITA"]], use_container_width=True)
else:
    st.error("A coluna 'DESCRIÇÃO DA FALHA' não foi encontrada no arquivo.")

# =========================
# ANÁLISE E VISUALIZAÇÃO
# =========================
st.header("📈 Estatísticas e Gráficos")

if "CATEGORIA_PREDITA" in df.columns:
    contagem = df["CATEGORIA_PREDITA"].value_counts()
    st.bar_chart(contagem)

    modelo_counts = df["MODELO"].value_counts()
    st.subheader("📦 Quantidade de defeitos por modelo")
    st.bar_chart(modelo_counts)

# =========================
# EXPORTAR RESULTADOS
# =========================
st.header("💾 Exportar Resultados")

if st.button("Salvar base classificada"):
    saida = "data/base_classificada.xlsx"
    df.to_excel(saida, index=False)
    st.success(f"Base salva em: `{saida}`")
