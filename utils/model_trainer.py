# ============================================
# utils/model_trainer.py
# ============================================
# Função de treinamento do modelo SIGMA-Q com feedback visual para o Streamlit
# ============================================

import pandas as pd
import joblib
import os
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import spacy

def treinar_modelo(base_path="data/base_de_dados.xlsx"):
    """
    Treina o modelo de classificação SIGMA-Q com base na planilha local.
    Retorna o modelo e o vetorizador treinados.
    """

    st.info("🚀 Iniciando treinamento do modelo SIGMA-Q...")

    if not os.path.exists(base_path):
        st.error(f"❌ Arquivo não encontrado: {base_path}")
        return None, None

    # Carrega dados
    df = pd.read_excel(base_path, engine="openpyxl")

    if "DESCRIÇÃO DA FALHA" not in df.columns or "CATEGORIA" not in df.columns:
        st.error("⚠️ Colunas obrigatórias não encontradas ('DESCRIÇÃO DA FALHA' e 'CATEGORIA').")
        return None, None

    # Pré-processamento
    df.dropna(subset=["DESCRIÇÃO DA FALHA", "CATEGORIA"], inplace=True)
    df["DESCRIÇÃO DA FALHA"] = df["DESCRIÇÃO DA FALHA"].astype(str)

    # NLP básico com spaCy
    nlp = spacy.load("pt_core_news_sm")
    df["texto_limpo"] = df["DESCRIÇÃO DA FALHA"].apply(lambda x: " ".join([t.lemma_ for t in nlp(x.lower()) if not t.is_stop]))

    st.progress(10)

    # Vetorização TF-IDF
    vetorizador = TfidfVectorizer(max_features=500)
    X = vetorizador.fit_transform(df["texto_limpo"])
    y = df["CATEGORIA"]

    st.progress(40)

    # Divide dados para treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treina o modelo
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train)

    st.progress(80)

    # Avaliação
    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    st.success(f"✅ Treinamento concluído com acurácia de {acc:.2%}")

    # Salva os modelos
    os.makedirs("model", exist_ok=True)
    joblib.dump(modelo, "model/modelo_classificacao.pkl")
    joblib.dump(vetorizador, "model/vectorizer.pkl")

    st.progress(100)
    st.toast("💾 Modelo e vetorizador salvos com sucesso!")
    st.info(f"📁 Caminho: model/modelo_classificacao.pkl")

    return modelo, vetorizador
