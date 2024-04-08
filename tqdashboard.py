import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('https://raw.githubusercontent.com/Rodrigoradzinski/Projeto-de-Circuitos-Digitais-Laborat-rio-e-Simula-o-IA--Predict_Match_World_Cups_2022-/main/WordCup_history_machs.csv')

#========================================================================================================   
# PADRAO COR ESCURO
#========================================================================================================

st.set_page_config(layout='wide')

st.title("História das Copas")

#========================================================================================================   
# PADRAO COR ESCU
#========================================================================================================




df['placar'] = df['placar'].str.replace('Ð', 'x')
df.rename(columns={
    'data_copa': 'Ano da Copa',
    'time_a': 'Time da Casa',
    'time_b': 'Time Visitante',
    'placar': 'Placar Final',
    'gols_do_time_da_casa': 'Gols Time da Casa',
    'gols_do_time_da_fora': 'Gols Time Visitante',
    'saldo_gols_do_time_da_casa': 'Saldo de Gols Time da Casa',
    'saldo_gols_do_time_da_fora': 'Saldo de Gols Time Visitante',
    'teve_prorrogacao': 'Houve Prorrogação?',
    'foi_para_penaltis': 'Houve Pênaltis?',
    'placar_penaltis': 'Placar dos Pênaltis',
    'gols_do_time_da_casa_penaltis': 'Gols Casa nos Pênaltis',
    'gols_do_time_da_fora_penaltis': 'Gols Visitante nos Pênaltis',
    'time_da_casa_vencedor': 'Vitória da Casa?',
    'time_da_fora_vencedor': 'Vitória Visitante?',
    'empatou': 'Empate?',
    'sede': 'País-Sede',
    'vencedor_copa': 'Campeão da Copa',
    'sede_vencedor': 'Sede Foi Campeã?',
    'qtd_times_parcticipantes': 'Total de Times'
}, inplace=True)





#definicoescores= 

cores_gradiente = ['#3F3163', '#3F3163', '#8366CF']

tab1, tab2, tab3, tab4 = st.tabs(["Resumo das Copas", "Análise de Partidas", "Desempenho dos Países", "Estatísticas de Gols"])

with tab1:
    st.header("Visão Geral das Copas do Mundo")
    st.write("Explore os dados gerais das Copas, incluindo os países anfitriões, os vencedores de cada edição e o número de times participantes.")
    
    
    st.markdown("---")
    
    ano_ultima_copa= '2022'
    total_copas = df['Ano da Copa'].nunique()
    primeiro_ano_copa = df['Ano da Copa'].min()
    total_gols = df['Gols Time da Casa'].sum() + df['Gols Time Visitante'].sum()
    total_times = df['Total de Times'].unique().sum()

    col1, col2, col3, col4 , col5= st.columns(5)
    
    col1.metric("Total de Copas", total_copas)
    col2.metric("Ano da Primeira Copa", primeiro_ano_copa)
    col3.metric("Ano da Ultima Copa", ano_ultima_copa) 
    col4.metric("Total de Gols", total_gols)
    col5.metric("Total de  Participantes", total_times)


    st.markdown("---")
    

#========================================================================================================   
# graico de pizza mosrar titulos dos paises
#========================================================================================================
   
            

    df_campeoes = df[['Ano da Copa', 'Campeão da Copa']].drop_duplicates()
    contagem_titulos = df_campeoes['Campeão da Copa'].value_counts().reset_index()
    contagem_titulos.columns = ['País', 'Número de Títulos']

    fig = go.Figure(data=[go.Pie(labels=contagem_titulos['País'],
                                values=contagem_titulos['Número de Títulos'],
                                pull=[0.1 if i == 0 else 0 for i in range(len(contagem_titulos))],  
                                textinfo='label+value',  
                                insidetextorientation='radial'  
                                )])

    fig.update_layout(
            title_text='Número de Títulos Mundiais por País',
            title_x=0.5,
            width=800,  
            height=600  
        )
            
    st.plotly_chart(fig, use_container_width=True)

#========================================================================================================   
# graico de linha numero de países participantes ao longo dos anos
#========================================================================================================
    st.markdown("---")
    df_participantes = df.groupby('Ano da Copa')['Total de Times'].max().reset_index()  
    fig_participantes = fig_participantes = px.line(
                            df_participantes, 
                            x='Ano da Copa', 
                            y='Total de Times', 
                            title='Número de Países Participantes ao longo dos anos', 
                            markers=True,
                            color_discrete_sequence=cores_gradiente 
                        )

    fig_participantes.update_layout(title_x=0.5, title_text='Número de Países Participantes ao Longo dos Anos')

#========================================================================================================   
# graico de número de gols por Copa
#========================================================================================================
    df_gols = df.groupby('Ano da Copa')[['Gols Time da Casa', 'Gols Time Visitante']].sum().reset_index()
    df_gols['Total Gols'] = df_gols['Gols Time da Casa'] + df_gols['Gols Time Visitante']
    fig_gols = px.bar(
                        df_gols, 
                        x='Ano da Copa', 
                        y='Total Gols', 
                        title='Número de Gols por Copa',
                        color='Total Gols',  
                        color_continuous_scale=cores_gradiente  
                    )
    fig_gols.update_layout(title_x=0.5, title_text='Número de Gols por Copa')


    

    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_participantes, use_container_width=True)
    with col2:
        st.plotly_chart(fig_gols, use_container_width=True)
        

    #st.dataframe(df[['Ano da Copa', 'País-Sede', 'Campeão da Copa', 'Total de Times']].drop_duplicates())

    #========================================================================================================   
    # DADOS DO BRASIL GERAL
    #========================================================================================================
    def calcular_fase(row):
        if row['Vitória da Casa?'] == 1 or row['Vitória Visitante?'] == 1:
            return 'Vitória'
        elif row['Empate?'] == 1:
            return 'Empate'
        else:
            return 'Derrota'
    df['Fase Alcançada'] = df.apply(calcular_fase, axis=1)
    ver_brasil = st.checkbox('Mostrar informações apenas do Brasil')

    if ver_brasil:
        st.header("Resumo de Desempenho do Brasil")   
        st.markdown("---")
        
        df_brasil = df[(df['Time da Casa'] == 'Brazil') | (df['Time Visitante'] == 'Brazil')]
        vitorias_brasil = (df_brasil['Vitória da Casa?'] == 1).sum() + (df_brasil['Vitória Visitante?'] == 1).sum()
        gols_marcados_brasil = df_brasil['Gols Time da Casa'].sum() + df_brasil['Gols Time Visitante'].sum()
        gols_sofridos_brasil = df_brasil['Gols Time Visitante'].sum() + df_brasil['Gols Time da Casa'].sum()

        col1, col2, col3 = st.columns(3)
        
        col1.metric("Vitórias do Brasil", vitorias_brasil)
        col2.metric("Gols Marcados pelo Brasil", gols_marcados_brasil)
        col3.metric("Gols Sofridos pelo Brasil", gols_sofridos_brasil)
        
        st.markdown("---")

        df_brasil = df[(df['Time da Casa'] == 'Brazil') | (df['Time Visitante'] == 'Brazil')]

        vitorias_por_ano = df_brasil[df_brasil['Campeão da Copa'] == 'Brazil'].groupby('Ano da Copa').size().reset_index(name='Vitórias')
        gols_marcados = df_brasil.groupby('Ano da Copa')['Gols Time da Casa'].sum().reset_index()
        gols_sofridos = df_brasil.groupby('Ano da Copa')['Gols Time Visitante'].sum().reset_index()


        fig_vitorias = px.bar(vitorias_por_ano, x='Ano da Copa', y='Vitórias', title='Vitórias do Brasil por Ano')
        fig_gols_marcados = px.line(gols_marcados, x='Ano da Copa', y='Gols Time da Casa', title='Gols Marcados pelo Brasil por Ano')
        fig_gols_sofridos = px.line(gols_sofridos, x='Ano da Copa', y='Gols Time Visitante', title='Gols Sofridos pelo Brasil por Ano')

        # Apresentação dos gráficos na aba do Brasil
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_vitorias, use_container_width=True)
        col2.plotly_chart(fig_gols_marcados, use_container_width=True)
        col1.plotly_chart(fig_gols_sofridos, use_container_width=True)
#========================================================================================================   
# gNova aba
#========================================================================================================

with tab2:
    st.header("Análise Detalhada de Partidas")
    st.write("Detalhe das partidas, incluindo jogos com maior número de gols, partidas que foram para prorrogação e pênaltis, e jogos com maior diferença de gols.")
     # Gráfico de Barras - Gols por Partida
    df['Total Gols por Partida'] = df['Gols Time da Casa'] + df['Gols Time Visitante']
    fig_gols_partida = px.histogram(df, x='Total Gols por Partida', nbins=20, title="Distribuição de Gols por Partida")
    st.plotly_chart(fig_gols_partida, use_container_width=True)
    
    # Gráfico de Linhas - Partidas com Prorrogação e Pênaltis por Copa
    df_prorrogacao_penaltis = df.groupby('Ano da Copa').agg({'Houve Prorrogação?':'sum', 'Houve Pênaltis?':'sum'}).reset_index()
    fig_prorrogacao_penaltis = px.line(df_prorrogacao_penaltis, x='Ano da Copa', y=['Houve Prorrogação?', 'Houve Pênaltis?'], title="Partidas com Prorrogação e Pênaltis por Copa")
    st.plotly_chart(fig_prorrogacao_penaltis, use_container_width=True)
    

with tab3:
    st.header("Desempenho dos Países ao longo das Copas")
    st.write("Análise do desempenho histórico de diferentes seleções nacionais, incluindo número de vitórias, gols marcados e sofridos.")
    # Adicionar aqui o código para os gráficos de desempenho dos países

with tab4:
    st.header("Estatísticas de Gols")
    st.write("Análise de gols por Copa, média de gols por partida e comparação entre gols do time da casa e time visitante.")
    
    # Gráfico de barras dos gols totais por Copa
    df_gols_por_copa = df.groupby('Ano da Copa', as_index=False)[['Gols Time da Casa', 'Gols Time Visitante']].sum()
    df_gols_por_copa['total_gols'] = df_gols_por_copa['Gols Time da Casa'] + df_gols_por_copa['Gols Time Visitante']
    fig_gols = px.bar(df_gols_por_copa, x='Ano da Copa', y='total_gols', title="Gols Totais por Copa", labels={'total_gols': 'Total de Gols', 'Ano da Copa': 'Ano da Copa'})
    st.plotly_chart(fig_gols, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("Desenvolvido por Equipe: Cleyton Rodrigo e Douglas.")
