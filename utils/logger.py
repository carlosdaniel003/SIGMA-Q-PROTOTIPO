# ============================================
# utils/logger.py
# ============================================
# Função: registrar automaticamente as classificações feitas pela IA
# Autor: Carlos Daniel (Projeto SIGMA-Q)
# ============================================

import pandas as pd
from datetime import datetime
import os

def registrar_classificacoes(df, arquivo_log="data/logs/log_classificacoes.xlsx"):
    """
    Adiciona as novas classificações feitas à planilha de log histórico.

    Args:s
        df (pd.DataFrame): DataFrame contendo pelo menos as colunas
                           ['DESCRIÇÃO DA FALHA', 'CATEGORIA_PREDITA'].
        arquivo_log (str): Caminho do arquivo Excel de log.
    """
    try:
        # Garante que a pasta de logs exista
        os.makedirs(os.path.dirname(arquivo_log), exist_ok=True)

        # Adiciona timestamp à classificação atual
        df_log = df.copy()
        df_log["DATA_LOG"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Se já existe um log anterior, concatenar
        if os.path.exists(arquivo_log):
            antigo = pd.read_excel(arquivo_log)
            combinado = pd.concat([antigo, df_log], ignore_index=True)
        else:
            combinado = df_log

        # Salva o log atualizado
        combinado.to_excel(arquivo_log, index=False)
        print(f"📁 Log atualizado com {len(df_log)} novos registros -> {arquivo_log}")

    except Exception as e:
        print(f"❌ Erro ao registrar log: {e}")
