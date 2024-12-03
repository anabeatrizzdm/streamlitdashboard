import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db import get_connection

# Título do dashboard
st.title("Dashboard de Alocação Acadêmica")

# Função para carregar os dados de uma tabela específica
def carregar_dados_tabela(tabela):
    connection = get_connection()
    if not connection:
        st.error("Erro ao conectar ao banco de dados.")
        return None

    try:
        query = f"SELECT * FROM {tabela}"
        df = pd.read_sql(query, connection)
        if df.empty:
            st.warning(f"A tabela '{tabela}' não contém dados.")
        else:
            st.write("dados carregados:")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

# Lista de tabelas disponíveis
tabelas = ["Materia", "Turma", "Alocacao", "Sala"]

# Menu lateral para selecionar a tabela
tabela_selecionada = st.sidebar.selectbox("Selecione a tabela para visualizar os dados", tabelas)

# Carregar os dados da tabela selecionada
df = carregar_dados_tabela(tabela_selecionada)

# Verificar se os dados foram carregados com sucesso
if df is not None:
    st.write(f"### Tabela: {tabela_selecionada}")
    # Exibir dados sem fazer nenhuma transformação de índice
    st.dataframe(df)

    if tabela_selecionada == "Sala":
        st.subheader("Análises para a Tabela 'Sala'")

        # Selecionar uma sala específica
        sala = df['id'].unique()
        sala_selecionada = st.selectbox("Selecione uma sala", sala)
        st.write(df[df['id'] == sala_selecionada])

        # Gráficos
        st.subheader("Número de Salas por Campus")
        salas_por_campus = df['campus_id'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=salas_por_campus.index, y=salas_por_campus.values, ax=ax)
        ax.set_xlabel("Campus")
        ax.set_ylabel("Número de Salas")
        st.pyplot(fig)

    elif tabela_selecionada == "Materia":
        st.subheader("Detalhes das Matérias")

        # Verificar se o DataFrame contém a coluna 'nome'
        if 'nome' not in df.columns:
            st.error("A tabela não contém a coluna 'nome'. Verifique os dados.")
        else:
            # Selecionar uma matéria específica
            materias = df['nome'].dropna().unique()
            materia_selecionada = st.selectbox("Selecione uma matéria", materias)
            st.write(df[df['nome'] == materia_selecionada])

        # Verificar se as colunas necessárias estão presentes
        if 'area' in df.columns:
            st.subheader("Número de Matérias por Área")
            materias_por_area = df['area'].value_counts()
            st.bar_chart(materias_por_area)
        else:
            st.warning("A coluna 'area' não está presente na tabela.")

        if 'semestre' in df.columns:
            st.subheader("Número de Matérias por Semestre")
            materias_por_semestre = df['semestre'].value_counts()
            st.bar_chart(materias_por_semestre)
        else:
            st.warning("A coluna 'semestre' não está presente na tabela.")

    elif tabela_selecionada == "Alocacao":
        st.subheader("Alocações")
        st.write("Colunas disponíveis na tabela 'Alocacao':", df.columns)
        st.write("Exemplo de dados:", df.head())

        st.subheader("Número de Alocações por Matéria")
        alocacoes_por_materia = df['materia_id'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=alocacoes_por_materia.index, y=alocacoes_por_materia.values, ax=ax, palette="coolwarm")
        ax.set_xlabel("ID da Matéria")
        ax.set_ylabel("Número de Alocações")
        st.pyplot(fig)
        
    elif tabela_selecionada == "Turma":
        st.subheader("Análises para a Tabela 'Turma'")

        # Gráfico 1: Número de Turmas por Semestre
        st.subheader("Número de Turmas por Semestre")
        turmas_por_semestre = df['semestre'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=turmas_por_semestre.index, y=turmas_por_semestre.values, ax=ax, palette="viridis")
        ax.set_xlabel("Semestre")
        ax.set_ylabel("Número de Turmas")
        st.pyplot(fig)

        # Gráfico 3: Número de Turmas por Turno
        st.subheader("Número de Turmas por Turno")
        turmas_por_turno = df['turno'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=turmas_por_turno.index, y=turmas_por_turno.values, ax=ax, palette="magma")
        ax.set_xlabel("Turno")
        ax.set_ylabel("Número de Turmas")
        st.pyplot(fig)

        # Gráfico 4: Número de Turmas por Campus
        st.subheader("Número de Turmas por Campus")
        turmas_por_campus = df['campus_id'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=turmas_por_campus.index, y=turmas_por_campus.values, ax=ax, palette="cividis")
        ax.set_xlabel("ID do Campus")
        ax.set_ylabel("Número de Turmas")
        st.pyplot(fig)

else:
    st.error("Não foi possível carregar os dados da tabela selecionada.")