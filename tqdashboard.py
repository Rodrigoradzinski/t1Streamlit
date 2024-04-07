# Salve este código em um arquivo, por exemplo, app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Carregando a base de dados (ajuste para o caminho do seu arquivo)
# Substitua 'seu_arquivo.csv' pelo caminho do seu arquivo CSV
df = pd.read_csv('https://raw.githubusercontent.com/Rodrigoradzinski/Projeto-de-Circuitos-Digitais-Laborat-rio-e-Simula-o-IA--Predict_Match_World_Cups_2022-/main/WordCup_history_machs.csv')
df.head(100)



# Configurando o layout da página
st.set_page_config(layout="wide")

# Cabeçalho
st.title("Análise das Copas do Mundo")

# Corpo
# Usaremos abas para organizar o conteúdo
tab1, tab2, tab3 = st.tabs(["Visão Geral", "Análise Detalhada", "Vendedores"])

with tab1:
    st.header("Dados Gerais das Copas")
    # Substitua por um dataframe relevante ou gráfico
    st.write(df.head())

with tab2:
    st.header("Análise de Gols por Copa")
    # Exemplo: Gráfico de barras dos gols totais por Copa
    df_gols_por_copa = df.groupby('data_copa')[['gols_do_time_da_casa', 'gols_do_time_da_fora']].sum().reset_index()
    df_gols_por_copa['total_gols'] = df_gols_por_copa['gols_do_time_da_casa'] + df_gols_por_copa['gols_do_time_da_fora']
    fig_gols = px.bar(df_gols_por_copa, x='data_copa', y='total_gols', title="Gols Totais por Copa")
    st.plotly_chart(fig_gols)

with tab3:
    st.header("Desempenho dos Vendedores")
    # Adicione análises ou visualizações específicas sobre os vendedores
    
    # Exemplo de filtro para selecionar vendedores
    vendedor = st.selectbox('Selecione o Vendedor:', df['vencedor_copa'].unique())
    df_vendedor = df[df['vencedor_copa'] == vendedor]
    st.write(df_vendedor)

# Rodapé
st.markdown("""
---
Desenvolvido por Equipe: Cleyton e Douglas.
            
""")

