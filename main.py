from utils import carregar_dados

print("🚀 Iniciando leitura da base...")
df = carregar_dados()  # ele vai procurar automaticamente o base_de_dados.xlsx
print("✅ Dados lidos com sucesso!")
print(df.head())
