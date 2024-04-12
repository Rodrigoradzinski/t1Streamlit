import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
from plotly.subplots import make_subplots

df = pd.read_csv('https://raw.githubusercontent.com/Rodrigoradzinski/Projeto-de-Circuitos-Digitais-Laborat-rio-e-Simula-o-IA--Predict_Match_World_Cups_2022-/main/WordCup_history_machs.csv')
st.set_page_config(layout='wide')
st.title("História das Copas")
df_geo = pd.read_csv('https://raw.githubusercontent.com/google/dspl/master/samples/google/canonical/countries.csv')

#========================================================================================================   
# AJUSTE NOS DADOS
#========================================================================================================
country_to_iso = {
        "Uruguay": "URY",
        "Italy": "ITA",
        "France": "FRA",
        "Brazil": "BRA",
        "Switzerland": "CHE",
        "Sweden": "SWE",
        "Chile": "CHL",
        "England": "GBR", 
        "Mexico": "MEX",
        "West Germany": "DEU",  
        "Argentina": "ARG",
        "Spain": "ESP",
        "United States": "USA",
        "Korea Japan": "KOR",  
        "Germany": "DEU",      
        "South Africa": "ZAF",
        "Russia": "RUS"
    }



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

#========================================================================================================   
# IMAGEMS BANDERIA
#========================================================================================================
#nome_selecao_unico = list(set(df['Time da Casa'].unique().tolist() + df['Time Visitante'].unique().tolist()))


Pais_name_iso = [
        'Brazil', 'Germany', 'Italy', 'Argentina', 'Uruguay', 'France', 'England', 'Spain', 
        'Mexico', 'Portugal', 'New Zealand', 'Bosnia and Herzegovina', 'Paraguay', 'Norway', 
        'Japan', 'Nigeria', 'United States', 'Slovakia', 'Jamaica', 'Croatia', 'Soviet Union', 
        'Republic of Ireland', 'Poland', 'Ghana', 'Saudi Arabia', 'Ecuador', 'Panama', 'South Korea', 
        'Haiti', 'Tunisia', 'Egypt', 'Turkey', 'Switzerland', 'Bulgaria', 'East Germany', 'Algeria', 
        'United Arab Emirates', 'Canada', 'Ivory Coast', 'Hungary', 'Greece', 'Czech Republic', 
        'Trinidad and Tobago', 'Ukraine', 'Denmark', 'Northern Ireland', 'Kuwait', 'Russia', 'South Africa', 
        'Honduras', 'Romania', 'Australia', 'Yugoslavia', 'Wales', 'Costa Rica', 'Slovenia', 
        'El Salvador', 'Sweden', 'Iran', 'West Germany', 'Cuba', 'Peru', 'Belgium', 'Colombia', 
        'Czechoslovakia', 'Bolivia', 'Netherlands', 'Scotland', 'Zaire', 'Angola', 'Israel', 
        'North Korea', 'Cameroon', 'Serbia and Montenegro', 'Togo', 'Austria', 'Serbia', 'Morocco', 
        'Iceland', 'Iraq', 'Dutch East Indies', 'China', 'Chile', 'Senegal', 'Uruguay'
    ]

Nome_em_Portugues=  [
        'Brasil', 'Alemanha', 'Itália', 'Argentina', 'Uruguai', 'França', 'Inglaterra', 'Espanha', 
        'México', 'Portugal', 'Nova Zelândia', 'Bósnia e Herzegovina', 'Paraguai', 'Noruega', 
        'Japão', 'Nigéria', 'Estados Unidos', 'Eslováquia', 'Jamaica', 'Croácia', 'União Soviética', 
        'República da Irlanda', 'Polônia', 'Gana', 'Arábia Saudita', 'Equador', 'Panamá', 'Coreia do Sul', 
        'Haiti', 'Tunísia', 'Egito', 'Turquia', 'Suíça', 'Bulgária', 'Alemanha Oriental', 'Argélia', 
        'Emirados Árabes Unidos', 'Canadá', 'Costa do Marfim', 'Hungria', 'Grécia', 'República Tcheca', 
        'Trinidad e Tobago', 'Ucrânia', 'Dinamarca', 'Irlanda do Norte', 'Kuwait', 'Rússia', 'África do Sul', 
        'Honduras', 'Romênia', 'Austrália', 'Iugoslávia', 'País de Gales', 'Costa Rica', 'Eslovênia', 
        'El Salvador', 'Suécia', 'Irã', 'Alemanha Ocidental', 'Cuba', 'Peru', 'Bélgica', 'Colômbia', 
        'Tchecoslováquia', 'Bolívia', 'Holanda', 'Escócia', 'Zaire', 'Angola', 'Israel', 
        'Coreia do Norte', 'Camarões', 'Sérvia e Montenegro', 'Togo', 'Áustria', 'Sérvia', 'Marrocos', 
        'Islândia', 'Iraque', 'Índias Orientais Holandesas', 'China', 'Chile', 'Senegal', 'Uruguai' 
    ]

vitorias_mundiais = [
    5, 4, 4, 2, 2, 2, 1, 1, 
] + [0] * (len(Pais_name_iso) - 8)


Bandeira_URL = [
    'https://static.significados.com.br/foto/brasil-6f.jpg',
    'https://static.significados.com.br/foto/alemanha.jpg',
    'https://static.significados.com.br/foto/bandeira-italia-0-cke.jpg',
    'https://static.significados.com.br/foto/argentina.jpg',
    'https://static.significados.com.br/foto/bandeira-do-uruguai-significados.jpg',
    'https://static.significados.com.br/foto/franca.jpg',
    'https://static.significados.com.br/foto/inglaterra.jpg',
    'https://static.significados.com.br/foto/espanha.jpg'
] + [''] * (len(Pais_name_iso) - 8)


df_completo_links_bandeira = pd.DataFrame({
    'Pais_name_iso': Pais_name_iso,
    'País': Nome_em_Portugues,  
    'Vitórias': vitorias_mundiais,
    'Bandeira_URL': Bandeira_URL
})
#E
df_vitorias = df_completo_links_bandeira[df_completo_links_bandeira['Vitórias'] > 0].reset_index(drop=True)
cores_gradiente = ['#3F3163', '#3F3163', '#8366CF']
cor_unica = ['#8e7cc3']



#========================================================================================================   
# funcoes
#========================================================================================================
def criar_cabecalho_cartao(titulo):
    st.markdown(f"""
        <div style="
            border-radius: 8px 8px 0 0;
            background-color: #333333;
            padding: 10px;
            color: white;
            font-size: 24px;
            text-align: center;
            margin-top: 10px;
            ">
            {titulo}
        </div>
        """, unsafe_allow_html=True)
    

def configurar_layout(fig):
    fig.update_layout(
        title={
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        title_font=dict(size=27),
        xaxis=dict(
            title_font=dict(size=18),  
            tickfont=dict(size=14),  
            tickangle=45,  
        ),
        yaxis=dict(
            title_font=dict(size=18), 
            tickfont=dict(size=14),  
             gridcolor='rgba(150,150,150,0.3)',  
        ),
        
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='rgba(0,0,0,0.0)',
        paper_bgcolor='rgba(0,0,0,0.3)',
        
        # Configurações da legenda
        legend=dict(
            title_font=dict(size=16), 
            font=dict(size=14),  
            bgcolor='rgba(0,0,0,0)',  
            bordercolor='rgba(100,100,100,0)',  
        ),
        
        
        hoverlabel=dict(
            font_size=16, 
        ),
    )
    
    st.markdown(
        """
        <style>
        .js-plotly-plot .plotly {
            border-radius: 25px;  
            overflow: hidden;    
           
        }
        .main .block-container {
        background-color: transparent !importante; 
        }
        </style>
        """
        , unsafe_allow_html=True
    )

    return fig



def calcular_fase(row):
        if row['Vitória da Casa?'] == 1 or row['Vitória Visitante?'] == 1:
            return 'Vitória'
        elif row['Empate?'] == 1:
            return 'Empate'
        else:
            return 'Derrota'
    

def mapear_para_cor(valor):
    if valor == 0:
        return "#bf9de2"  
    elif valor == 1:
        return "#5bb3d9"  
    elif valor <= 3:
        return "#F73232"  
    else:
        return "#FF0000"  
    

def metrica_personalizada(titulo, valor):
    st.markdown(f"<h3 style='text-align: center; color: white;'>{titulo}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: white;'>{valor}</h3>", unsafe_allow_html=True)

#========================================================================================================   
# CRIANDO CORES PARA GRAFCO
#========================================================================================================


tab1, tab2, tab3, tab4 ,tab5= st.tabs(["Resumo das Copas","Desempenho dos Países", "Comparativo entre Seleções",  "Estatísticas de Gols","Análise de Partidas"])
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
    
    with col1:
        metrica_personalizada("Total de Copas", total_copas)
    with col2:
        metrica_personalizada("Ano da Primeira Copa", primeiro_ano_copa)
    with col3:
        metrica_personalizada("Ano da Ultima Copa", ano_ultima_copa) 
    with col4:
        metrica_personalizada("Total de Gols", total_gols)
    with col5:
        metrica_personalizada("Total de  Participantes", total_times)      

    st.markdown("---")
    
    #st.dataframe(df_geo[['country','latitude','longitude','name']])
    #st.dataframe(df[['País-Sede','Campeão da Copa']])
    
    contagem_sedes = df.groupby('País-Sede')['Ano da Copa'].nunique().reset_index(name='Contagem de Sedes')
    uniao_df_df_geo = pd.merge(df_geo, contagem_sedes, left_on='name', right_on='País-Sede', how='left')
    uniao_df_df_geo['Contagem de Sedes'] = uniao_df_df_geo['Contagem de Sedes'].fillna(0)
    sedes_copa = uniao_df_df_geo[uniao_df_df_geo['Contagem de Sedes'] > 0]
    sedes_copa.loc[:, 'size'] = sedes_copa['Contagem de Sedes'] * 100000
    sedes_copa.loc[:, 'color'] = sedes_copa['Contagem de Sedes'].apply(mapear_para_cor)
    num_colunas = len(df_vitorias['País'])  
    cols = st.columns(num_colunas)

    for i, row in df_vitorias.iterrows():
        with cols[i]:
            st.markdown(f"""
                <div style='text-align: center; color: white;'>
                    <img src='{row['Bandeira_URL']}' alt='Bandeira' style='height:50px; margin-bottom:10px;'><br>
                    <h3>{row['País']}</h3>
                    <h4>{row['Vitórias']}</h4>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    mapa1= st.map(data=sedes_copa, latitude='latitude', longitude='longitude', color='color', size='size')
    
#========================================================================================================   
# graico de linha numero de países participantes ao longo dos anos
#========================================================================================================
    st.markdown("---")
    df_participantes = df.groupby('Ano da Copa')['Total de Times'].max().reset_index()  
    fig_participantes = fig_participantes = px.line(
                            df_participantes, 
                            x='Ano da Copa', 
                            y='Total de Times', 
                            title='Número de Países Participantes', 
                            markers=True,
                            color_discrete_sequence=cores_gradiente 
                        )

    fig_participantes.update_layout(title_x=0.5, title_text='Número de Países Participantes')
    fig_participantes = configurar_layout(fig_participantes)
    

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
    
    fig_gols = configurar_layout(fig_gols)




    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_participantes, use_container_width=True)
    with col2:
        
        st.plotly_chart(fig_gols, use_container_width=True)
    #st.dataframe(df[['Ano da Copa', 'País-Sede', 'Campeão da Copa', 'Total de Times']].drop_duplicates())
#========================================================================================================   
# gNova aba
#========================================================================================================
with tab2:
    st.header("Análise Detalhada de Seleções")
    st.write("Detalhe das Seleções, incluindo jogos com maior número de gols, partidas que foram para prorrogação e pênaltis, e jogos com maior diferença de gols.")

    
    def calcular_fase(row):
        if row['Vitória da Casa?'] == 1 or row['Vitória Visitante?'] == 1:
            return 'Vitória'
        elif row['Empate?'] == 1:
            return 'Empate'
        else:
            return 'Derrota'

    
    def metrica_personalizada(label, valor):
        st.metric(label=label, value=valor)

    
    def recalcular_estatisticas(df, selecoes_escolhidas):
        df_filtrado = df[(df['Time da Casa'].isin(selecoes_escolhidas)) | (df['Time Visitante'].isin(selecoes_escolhidas))]
        df_filtrado['Fase Alcançada'] = df_filtrado.apply(calcular_fase, axis=1)
        df_filtrado['Identificador do Jogo'] = df_filtrado['Ano da Copa'].astype(str) + ' - ' + df_filtrado['Time da Casa'] + ' vs ' + df_filtrado['Time Visitante']
        df_filtrado['Diferença de Gols'] = abs(df_filtrado['Gols Time da Casa'] - df_filtrado['Gols Time Visitante'])
        return df_filtrado

    
    selecoes_unicas = list(set(df['Time da Casa'].unique().tolist() + df['Time Visitante'].unique().tolist()))
    print(selecoes_unicas)
    default_selecao = ['Brazil'] if 'Brazil' in selecoes_unicas else []
    selecoes_escolhidas = st.multiselect('Escolha as seleções para análise:', selecoes_unicas, default=default_selecao)

    
    if selecoes_escolhidas:
        df_filtrado = recalcular_estatisticas(df, selecoes_escolhidas)
        
        st.header(f"Resumo de Desempenho das Seleções Escolhidas")
        st.markdown("---")

        
        prorrogacoes = df_filtrado[df_filtrado['Houve Prorrogação?'] == 1]
        penaltis = df_filtrado[df_filtrado['Houve Pênaltis?'] == 1]
        
        prorrogacoes_por_ano = prorrogacoes.groupby('Ano da Copa').size().reset_index(name='Partidas com Prorrogação')
        penaltis_por_ano = penaltis.groupby('Ano da Copa').size().reset_index(name='Partidas com Penáltis')

        jogos_diferenca_gols = df_filtrado.nlargest(5, 'Diferença de Gols')
        vitorias_por_ano = df_filtrado[df_filtrado['Fase Alcançada'] == 'Vitória'].groupby('Ano da Copa').size().reset_index(name='Vitórias')
        gols_marcados_por_ano = df_filtrado.groupby('Ano da Copa')['Gols Time da Casa'].sum().reset_index()
        gols_sofridos_por_ano = df_filtrado.groupby('Ano da Copa')['Gols Time Visitante'].sum().reset_index()


    
        
        fig_prorrogacoes = px.line(prorrogacoes_por_ano, x='Ano da Copa', y='Partidas com Prorrogação', title='Partidas com Prorrogação por Ano', line_shape='linear', color_discrete_sequence=cor_unica)
        fig_penaltis = px.line(penaltis_por_ano, x='Ano da Copa', title='Partidas Decididas por Pênaltis por Ano', line_shape='linear', color_discrete_sequence=cor_unica)
        fig_gols_marcados = px.line(gols_marcados_por_ano, x='Ano da Copa', y='Gols Time da Casa', title='Gols Marcados por Ano', line_shape='linear', color_discrete_sequence=cor_unica)
        fig_gols_sofridos = px.line(gols_sofridos_por_ano, x='Ano da Copa', y='Gols Time Visitante', title='Gols Sofridos por Ano', line_shape='linear', color_discrete_sequence=cor_unica)

       
        fig_diferenca_gols = px.bar(jogos_diferenca_gols, x='Identificador do Jogo', y='Diferença de Gols', title='Jogos com Maior Diferença de Gols', color_discrete_sequence=cor_unica)
        fig_vitorias = px.bar(vitorias_por_ano, x='Ano da Copa', y='Vitórias', title='Vitórias por Ano', color_discrete_sequence=cor_unica)
       
        fig_prorrogacoes = configurar_layout (fig_prorrogacoes)
        fig_penaltis = configurar_layout (fig_penaltis)
        fig_gols_marcados = configurar_layout (fig_gols_marcados)
        fig_gols_sofridos = configurar_layout (fig_gols_sofridos)
        fig_diferenca_gols = configurar_layout (fig_diferenca_gols)
        fig_vitorias = configurar_layout (fig_vitorias)

     
        
#========================================================================================================   
# 
#========================================================================================================



        
        colunas = st.columns(6)
        metricas = [
            ("Vitórias", (df_filtrado['Fase Alcançada'] == 'Vitória').sum()),
            ("Gols Marcados", df_filtrado['Gols Time da Casa'].sum() + df_filtrado['Gols Time Visitante'].sum()),
            ("Gols Sofridos", df_filtrado[df_filtrado['Time da Casa'].isin(selecoes_escolhidas)]['Gols Time Visitante'].sum() + df_filtrado[df_filtrado['Time Visitante'].isin(selecoes_escolhidas)]['Gols Time da Casa'].sum()),
            ("Empates", (df_filtrado['Fase Alcançada'] == 'Empate').sum()),
            ("Prorrogação", prorrogacoes['Houve Prorrogação?'].sum()),
            ("Penaltis", penaltis['Houve Pênaltis?'].sum())
        ]
        for col, (label, valor) in zip(colunas, metricas):
            with col:
                metrica_personalizada(label, valor)

        if st.checkbox('Mostrar Detalhes'):
            st.dataframe(prorrogacoes)


        st.markdown('---', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_vitorias, use_container_width=True)
        col2.plotly_chart(fig_gols_marcados, use_container_width=True)

        st.markdown('---', unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        col3.plotly_chart(fig_gols_sofridos, use_container_width=True)
        col4.plotly_chart(fig_prorrogacoes, use_container_width=True)

        st.markdown('---', unsafe_allow_html=True)

        col5, col6 = st.columns(2)
        col5.plotly_chart(fig_penaltis, use_container_width=True)
        col6.plotly_chart(fig_diferenca_gols, use_container_width=True)
    else:
        st.write("Nenhuma seleção escolhida.")

       
      
#========================================================================================================   
# graico de linha numero de países participantes ao longo dos anos
#========================================================================================================


if 'Vencedor' not in df.columns:
    df['Vencedor'] = df.apply(lambda row: row['Time da Casa'] if row['Gols Time da Casa'] > row['Gols Time Visitante'] 
                              else (row['Time Visitante'] if row['Gols Time da Casa'] < row['Gols Time Visitante'] 
                                    else 'Empate'), axis=1)

df_estatisticas = pd.DataFrame({
    'Selecao': pd.concat([df['Time da Casa'], df['Time Visitante']]).unique()
})

vitorias = df[df['Vencedor'] != 'Empate']['Vencedor'].value_counts()
df_estatisticas['Vitorias'] = df_estatisticas['Selecao'].map(vitorias).fillna(0)

df_estatisticas['Participacoes'] = df_estatisticas['Selecao'].apply(lambda x: len(set(df[df['Time da Casa'] == x]['Ano da Copa']).union(set(df[df['Time Visitante'] == x]['Ano da Copa']))))
df_estatisticas['Gols Marcados'] = df_estatisticas['Selecao'].apply(lambda x: df[df['Time da Casa'] == x]['Gols Time da Casa'].sum() + df[df['Time Visitante'] == x]['Gols Time Visitante'].sum())
df_estatisticas['Gols Sofridos'] = df_estatisticas['Selecao'].apply(lambda x: df[df['Time da Casa'] == x]['Gols Time Visitante'].sum() + df[df['Time Visitante'] == x]['Gols Time da Casa'].sum())
df_estatisticas['Diferenca Gols'] = df_estatisticas['Gols Marcados'] - df_estatisticas['Gols Sofridos']



df_estatisticas = df_estatisticas.merge(df_completo_links_bandeira, how='left', left_on='Selecao', right_on='Pais_name_iso')
#st.dataframe(df_estatisticas)
top_10_vitorias = df_estatisticas.sort_values('Vitorias', ascending=False).head(10)
top_10_participacoes = df_estatisticas.sort_values('Participacoes', ascending=False).head(10)
top_10_gols_marcados = df_estatisticas.sort_values('Gols Marcados', ascending=False).head(10)
top_10_gols_sofridos = df_estatisticas.sort_values('Gols Sofridos', ascending=False).head(10)  
top_10_diferenca_gols = df_estatisticas.sort_values('Diferenca Gols', ascending=False).head(10)

   st.dataframe(df_filtrado)

#========================================================================================================   
# 
#========================================================================================================



with tab3:
   
    st.header("Comparativo entre Seleções")
    st.write("Aqui podemos criar comparativos entre seleções que já disputaram copas.")
    metrica_comparativa = st.selectbox('Escolha uma métrica para comparação:', 
                                       ['Vitórias', 'Participações em Copas do Mundo', 'Gols Marcados', 'Gols Sofridos', 'Diferença de Gols'])
    
    brasil_stats = df_estatisticas[df_estatisticas['Selecao'] == 'Brazil'].iloc[0]
 
    def criar_grafico(metrica, df_metrica):
        fig = go.Figure()
        if 'Brazil' in df_metrica['Selecao'].values:
            brasil_stats = df_metrica[df_metrica['Selecao'] == 'Brazil'].iloc[0]
            df_metrica = df_metrica[df_metrica['Selecao'] != 'Brazil'] 
            fig.add_trace(go.Bar(
                x=[brasil_stats[metrica]],
                y=['Brasil'],
                name='Brasil',
                marker=dict(color='#8366CF'),
                orientation='h',
                width=0.8,
                hovertemplate="Seleção: %{y}<br>Métrica: %{x}<extra></extra>",
            ))

        df_metrica = df_metrica.sort_values(by=metrica, ascending=False)
        for _, row in df_metrica.iterrows():
            fig.add_trace(go.Bar(
                x=[row[metrica]],
                y=[row['Selecao']],
                name=row['Selecao'],
                marker=dict(color='#3F3163'),
                width=0.9,
                orientation='h',
                hovertemplate="Seleção: %{y}<br>Métrica: %{x}<extra></extra>",
            ))

        fig.update_layout(
            title=f'Comparação de {metrica.replace("_", " ")}',
            barmode='overlay',
            yaxis=dict(categoryorder='total ascending'),
            xaxis_title=metrica.replace("_", " "),
            yaxis_title="Seleções",
            hovermode="y",
            height=800,
        )
        fig = configurar_layout(fig)
        fig.update_traces(hoverinfo='none')
        st.plotly_chart(fig, use_container_width=True)
        fig = configurar_layout(fig) 
    


    if metrica_comparativa == 'Vitórias':
        criar_grafico('Vitorias', top_10_vitorias)
    elif metrica_comparativa == 'Participações em Copas do Mundo':
        criar_grafico('Participacoes', top_10_participacoes)
    elif metrica_comparativa == 'Gols Marcados':
        criar_grafico('Gols Marcados', top_10_gols_marcados)
    elif metrica_comparativa == 'Gols Sofridos':
        criar_grafico('Gols Sofridos', top_10_gols_sofridos)
    elif metrica_comparativa == 'Diferença de Gols':
        criar_grafico('Diferenca Gols', top_10_diferenca_gols)
        

with tab4:
    st.header("Estatísticas de Gols")
    st.write("Análise de gols por Copa, média de gols por partida e comparação entre gols do time da casa e time visitante.")
    df_gols_por_copa = df.groupby('Ano da Copa', as_index=False)[['Gols Time da Casa', 'Gols Time Visitante']].sum()
    df_gols_por_copa['total_gols'] = df_gols_por_copa['Gols Time da Casa'] + df_gols_por_copa['Gols Time Visitante']
    fig_gols = px.bar(df_gols_por_copa, x='Ano da Copa', y='total_gols', title="Gols Totais por Copa", labels={'total_gols': 'Total de Gols', 'Ano da Copa': 'Ano da Copa'})
    fig_gols = configurar_layout (fig_gols)
    st.plotly_chart(fig_gols, use_container_width=True)
    st.dataframe(df_gols_por_copa)

with tab5:
    st.header("Análise Detalhada de Partidas")
    st.write("Detalhe das partidas, incluindo jogos com maior número de gols, partidas que foram para prorrogação e pênaltis, e jogos com maior diferença de gols.")
    df['Total Gols por Partida'] = df['Gols Time da Casa'] + df['Gols Time Visitante']
    fig_gols_partida = px.histogram(df, x='Total Gols por Partida', nbins=20, title="Distribuição de Gols por Partida")
    fig_gols_partida = configurar_layout (fig_gols_partida)
    st.plotly_chart(fig_gols_partida, use_container_width=True)
    
    df_prorrogacao_penaltis = df.groupby('Ano da Copa').agg({'Houve Prorrogação?':'sum', 'Houve Pênaltis?':'sum'}).reset_index()
    fig_prorrogacao_penaltis = px.line(df_prorrogacao_penaltis, x='Ano da Copa', y=['Houve Prorrogação?', 'Houve Pênaltis?'], title="Partidas com Prorrogação e Pênaltis por Copa")
    fig_prorrogacao_penaltis = configurar_layout (fig_prorrogacao_penaltis)
    st.plotly_chart(fig_prorrogacao_penaltis, use_container_width=True)
    st.dataframe(df_prorrogacao_penaltis)
    
# Rodapé
st.markdown("---")
st.markdown("Desenvolvido por Equipe: Cleyton Rodrigo e Douglas ®")
