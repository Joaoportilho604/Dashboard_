import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------- Gerar dados simulados --------
np.random.seed(42)

anos = list(range(2020, 2025))
ativos = ['ETF - Tech', 'ETF - Saúde', 'ETF - Energia', 'Ação - Apple', 'Ação - Amazon', 'Ação - Tesla']

dados = []
for ano in anos:
    for ativo in ativos:
        investimento = np.random.randint(5000, 20000)
        rendimento = investimento * (1 + np.random.uniform(-0.1, 0.3))  # entre -10% e +30%
        dados.append({
            'Ano': ano,
            'Ativo': ativo,
            'Investimento (€)': investimento,
            'Valor Atual (€)': round(rendimento, 2)
        })

df = pd.DataFrame(dados)
df['Retorno (%)'] = ((df['Valor Atual (€)'] - df['Investimento (€)']) / df['Investimento (€)']) * 100

# -------- Interface do Dashboard --------
st.set_page_config(page_title="Investimentos em ETFs e Ações", layout="wide")
st.title("📈 Investimentos em ETFs e Ações (2020 - 2024)")
st.markdown("Este dashboard apresenta uma visão geral dos investimentos simulados em ETFs e Ações nos últimos 5 anos.")

# Filtro por ano
anos_selecionados = st.multiselect("Filtrar por ano", options=anos, default=anos)
df_filtrado = df[df['Ano'].isin(anos_selecionados)]

# Gráfico de barras - Investimento total por ativo
invest_total = df_filtrado.groupby('Ativo')['Investimento (€)'].sum().reset_index()
fig1 = px.bar(invest_total, x='Ativo', y='Investimento (€)', title="Investimento Total por Ativo", color='Ativo')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de linhas - Evolução do valor atual
fig2 = px.line(df_filtrado, x='Ano', y='Valor Atual (€)', color='Ativo', title="Evolução do Valor Atual (€)")
st.plotly_chart(fig2, use_container_width=True)

# Tabela de Retornos
st.subheader("📊 Tabela Detalhada de Retornos")
st.dataframe(df_filtrado[['Ano', 'Ativo', 'Investimento (€)', 'Valor Atual (€)', 'Retorno (%)']])