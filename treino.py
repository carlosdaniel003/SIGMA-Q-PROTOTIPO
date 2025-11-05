import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import os

# Caminho do arquivo
caminho_arquivo = r"C:\Users\cdaniel\Documents\SIGMA-Q PROTÓTIPO\data\base_de_dados.xlsx"

print("🚀 Iniciando treinamento...")

# Leitura dos dados
df = pd.read_excel(caminho_arquivo)
print(f"✅ Dados carregados de: {caminho_arquivo}")
print(f"📊 Total de linhas: {len(df)}")

# Normaliza nomes das colunas (remove espaços extras)
df.columns = [c.strip() for c in df.columns]

# Define as colunas corretas com acento
col_texto = "DESCRIÇÃO DA FALHA"
col_categoria = "CATEGORIA"

# Verifica se as colunas existem
if col_texto not in df.columns or col_categoria not in df.columns:
    raise ValueError(f"❌ Colunas obrigatórias não encontradas: {col_texto}, {col_categoria}")

# Remove linhas vazias
df = df.dropna(subset=[col_texto, col_categoria])

# Caso tenha poucos dados, treina com todos
if len(df) < 5:
    print(f"⚠️ Base pequena detectada ({len(df)} linhas). Treinando com todos os dados disponíveis.")
    X_train = df[col_texto]
    y_train = df[col_categoria]
    X_test, y_test = X_train, y_train  # usa os mesmos dados só pra validar
else:
    # Divide base em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        df[col_texto], df[col_categoria], test_size=0.2, random_state=42
    )

# Vetorização do texto
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Treina modelo
modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_train_tfidf, y_train)

# Avalia
y_pred = modelo.predict(X_test_tfidf)
print("\n📈 Relatório de Classificação:")
print(classification_report(y_test, y_pred, zero_division=0))

# Salva modelo e vetorizador
os.makedirs("model", exist_ok=True)
joblib.dump(modelo, "model/modelo_classificacao.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("\n✅ Modelo e vetorizador salvos na pasta 'model'!")