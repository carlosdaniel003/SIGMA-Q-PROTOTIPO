import pandas as pd

arquivo = r"C:\Users\cdaniel\Documents\SIGMA-Q PROTÓTIPO\data\base_de_dados.xlsx"

df = pd.read_excel(arquivo)
print("🔍 Colunas encontradas no arquivo:")
for c in df.columns:
    print(f"- '{c}'")
