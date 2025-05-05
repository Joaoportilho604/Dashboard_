import streamlit as st
import pandas as pd
import plotly.express as px

# ----- DADOS SIMULADOS COM BASE EM DADOS REAIS -----
dados = {
    "Ano": [2020, 2021, 2022, 2023, 2024]*6,
    "Ativo": ["ETF - S&P 500"]*5 + ["ETF - MSCI World"]*5 + ["ETF - FTSE All-World"]*5 +
             ["Ação - Apple"]*5 + ["Ação - Microsoft"]*5 + ["Ação - Coca-Cola"]*5,
    "Valor Inicial (€)": [10000]*30,
    "Valor Final (€)": [
        # ETF - S&P 500
        10200, 11900, 10800, 12300, 12800,
        # ETF - MSCI World
        10100, 11700, 10700, 12000, 12600,
        # ETF - FTSE All-World
        9800, 11400, 10500, 11800, 12200,
        # Apple
        10300, 12500, 11200, 13000, 14000,
        # Microsoft
        10150, 12000, 11000, 12600, 13500,
        # Coca-Cola
        9900, 11200, 10600, 11500, 11800,
    ]
}

df = pd.DataFrame(dados)
df["Retorno (%)"] = ((df["Valor Final (€)"] - df["Valor Inicial (€)"]) / df["Valor Inicial (€)"]) * 100

# ----- CONFIGURAÇÃO STREAMLIT -----
st.set_page_config(page_title="Investimentos em ETFs e Ações", layout="wide")
st.title("📊 Investimentos em ETFs e Ações (2020 - 2024)")
st.markdown("Comparacão de performance de ativos populares com base em dados históricos dos últimos 5 anos.")

# ----- FILTROS -----
anos_disponiveis = df["Ano"].unique()
ativos_disponiveis = df["Ativo"].unique()

col1, col2 = st.columns(2)

with col1:
    anos_filtrados = st.multiselect("Selecionar ano(s)", anos_disponiveis, default=list(anos_disponiveis))

with col2:
    ativos_filtrados = st.multiselect("Selecionar ativo(s)", ativos_disponiveis, default=list(ativos_disponiveis))

df_filtrado = df[(df["Ano"].isin(anos_filtrados)) & (df["Ativo"].isin(ativos_filtrados))]

# ----- GRÁFICOS -----
st.subheader("📈 Evolução do Valor Final (€) por Ativo")
fig1 = px.line(df_filtrado, x="Ano", y="Valor Final (€)", color="Ativo", markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📉 Retorno (%) por Ativo e Ano")
fig2 = px.bar(df_filtrado, x="Ano", y="Retorno (%)", color="Ativo", barmode="group")
st.plotly_chart(fig2, use_container_width=True)

# ----- TABELA -----
st.subheader("📊 Tabela de Dados")
st.dataframe(df_filtrado, use_container_width=True)

# ----- MELHOR ATIVO POR ANO -----
st.subheader("🌟 Melhor ETF e Melhor Ação por Ano")

df_etf = df[df["Ativo"].str.contains("ETF")]
df_acao = df[df["Ativo"].str.contains("Ação")]

melhores_etfs = df_etf.loc[df_etf.groupby("Ano")["Retorno (%)"].idxmax()]
melhores_acoes = df_acao.loc[df_acao.groupby("Ano")["Retorno (%)"].idxmax()]

col3, col4 = st.columns(2)
with col3:
    st.markdown("### 🗓️ Melhor ETF por ano")
    st.dataframe(melhores_etfs[["Ano", "Ativo", "Retorno (%)"]].reset_index(drop=True))

with col4:
    st.markdown("### 🗓️ Melhor Ação por ano")
    st.dataframe(melhores_acoes[["Ano", "Ativo", "Retorno (%)"]].reset_index(drop=True))

# ----- MELHOR GERAL -----
melhor_etf_geral = df_etf.groupby("Ativo")["Retorno (%)"].mean().idxmax()
melhor_acao_geral = df_acao.groupby("Ativo")["Retorno (%)"].mean().idxmax()

st.subheader("🔹 Melhor ETF e Ação no total dos 5 anos")
col5, col6 = st.columns(2)
with col5:
    melhor_etf_valor = df_etf.groupby("Ativo")["Retorno (%)"].mean().max()
    st.success(f"**Melhor ETF:** {melhor_etf_geral} ({melhor_etf_valor:.2f}%)")

with col6:
    melhor_acao_valor = df_acao.groupby("Ativo")["Retorno (%)"].mean().max()
    st.success(f"**Melhor Ação:** {melhor_acao_geral} ({melhor_acao_valor:.2f}%)")

# ----- SIMULAÇÃO DE INVESTIMENTO -----
st.subheader("🧱 Simulação de Investimento")

valor_invest = st.number_input("Valor a investir (€)", min_value=10, value=200)
ano_inicio = st.selectbox("Ano de investimento", [2020, 2021,2022,2023])
ano_fim = st.selectbox("Ano final para ver retorno", [2021,2022,2023, 2024])
ativo_sim = st.selectbox("Selecionar ativo para simulação", ativos_disponiveis)

df_sim = df[(df["Ano"].isin([ano_inicio, ano_fim])) & (df["Ativo"] == ativo_sim)]

if len(df_sim) == 2:
    valor_inicial_real = df_sim[df_sim["Ano"] == ano_inicio]["Valor Final (€)"].values[0]
    valor_final_real = df_sim[df_sim["Ano"] == ano_fim]["Valor Final (€)"].values[0]

    retorno = valor_invest * (valor_final_real / valor_inicial_real)
    st.info(f"Se tivesse investido {valor_invest:.2f}€ em {ano_inicio} no ativo {ativo_sim}, teria aproximadamente {retorno:.2f}€ em {ano_fim}.")

    # ----- PREVISÃO PARA 6 MESES -----
    df_ativo = df[df["Ativo"] == ativo_sim].sort_values("Ano")
    crescimento_total = df_ativo["Valor Final (€)"].values[-1] / df_ativo["Valor Final (€)"].values[0]
    crescimento_mensal = crescimento_total ** (1/(5*12))
    valor_6_meses = retorno * (crescimento_mensal ** 6)

    st.success(f"📊 Estimativa para 6 meses seguintes: {valor_6_meses:.2f}€")
else:
    st.warning("Dados insuficientes para simulação com os anos selecionados.")
