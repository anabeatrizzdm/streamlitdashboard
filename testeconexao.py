import mysql.connector
import pandas as pd
from db import create_connection

def obter_dados_tabelas():
    connection = create_connection()
    if connection is None:
        print("Erro ao conectar ao banco de dados!")
        return None

    cursor = connection.cursor(dictionary=True)
    tabelas = {}

    # Recupera dados de todas as tabelas
    for tabela in ["Sala", "Materia", "Turno", "Campus", "Alocacao"]:
        cursor.execute(f"SELECT * FROM {tabela}")
        dados = cursor.fetchall()
        tabelas[tabela] = pd.DataFrame(dados)  # Converte diretamente para DataFrame

    cursor.close()
    connection.close()

    return tabelas