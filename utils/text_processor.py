# ============================================
# utils/text_processor.py
# ============================================
# Funções de pré-processamento de texto para o SIGMA-Q
# Responsável por limpar, normalizar e lematizar
# descrições de falhas antes do treinamento e inferência.
# ============================================

import re
import unicodedata
import pandas as pd

try:
    import spacy
except ImportError:
    spacy = None


# =========================
# CARREGAMENTO DO MODELO spaCy
# =========================
def carregar_spacy_modelo():
    """
    Carrega o modelo de linguagem em português do spaCy.
    Faz fallback automático caso o modelo não esteja instalado.
    """
    if not spacy:
        print("⚠️ spaCy não instalado. Pré-processamento limitado.")
        return None

    try:
        nlp = spacy.load("pt_core_news_sm")
        print("✅ Modelo spaCy 'pt_core_news_sm' carregado com sucesso!")
        return nlp
    except Exception as e:
        print(f"⚠️ Erro ao carregar modelo spaCy: {e}")
        print("Tentando baixar automaticamente...")
        try:
            from spacy.cli import download
            download("pt_core_news_sm")
            nlp = spacy.load("pt_core_news_sm")
            print("✅ Modelo spaCy instalado e carregado.")
            return nlp
        except Exception as e2:
            print(f"❌ Falha ao baixar o modelo spaCy: {e2}")
            return None


# =========================
# LIMPEZA DE TEXTO
# =========================
def limpar_texto(texto: str) -> str:
    """
    Limpa e padroniza o texto removendo ruídos, acentos e pontuações.
    """
    if not isinstance(texto, str):
        return ""

    # Normaliza acentuação
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")

    # Remove caracteres especiais e múltiplos espaços
    texto = re.sub(r"[^a-zA-Z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip().lower()


# =========================
# LEMATIZAÇÃO COM spaCy
# =========================
def lematizar_texto(texto: str, nlp_model=None) -> str:
    """
    Lematiza um texto utilizando o modelo spaCy.
    Caso o modelo não esteja disponível, retorna o texto limpo.
    """
    texto_limpo = limpar_texto(texto)

    if not nlp_model:
        return texto_limpo

    doc = nlp_model(texto_limpo)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)


# =========================
# PRÉ-PROCESSAMENTO EM LOTE
# =========================
def preprocessar_dataframe(df: pd.DataFrame, coluna_texto="DESCRIÇÃO DA FALHA") -> pd.DataFrame:
    """
    Aplica limpeza e lematização em toda a coluna de descrições.
    Retorna o DataFrame atualizado com uma nova coluna 'TEXTO_PROCESSADO'.
    """
    if coluna_texto not in df.columns:
        raise ValueError(f"Coluna '{coluna_texto}' não encontrada no DataFrame.")

    nlp = carregar_spacy_modelo()

    textos_processados = [
        lematizar_texto(texto, nlp_model=nlp)
        for texto in df[coluna_texto].astype(str)
    ]

    df["TEXTO_PROCESSADO"] = textos_processados
    print(f"✅ {len(df)} textos processados com sucesso.")
    return df
