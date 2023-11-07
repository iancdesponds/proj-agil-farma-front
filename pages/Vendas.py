import streamlit as st
import requests
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page
from time import sleep
import pandas as pd
import scipy
import plotly.figure_factory as ff
import plotly.express as px

st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_title="Vendas")

show_pages(
    [
        Page("pages/Menu.py", "Home"),
        Page("pages/Produtos.py", "Produtos"),
        Page("pages/Estoque.py", "Estoque"),
        Page("pages/Vendas.py", "Vendas"),
    ]
)

st.title("Vendas")

if st.sidebar.button("Logout"):
    try:
        st.sidebar.success("Logout bem-sucedido.")
        sleep(1)
        show_pages(
            [
                Page("pages/Menu.py", "Home"),
                Page("pages/Produtos.py", "Produtos"),
                Page("pages/Estoque.py", "Estoque"),
                Page("pages/Vendas.py", "Vendas"),
                Page("Main.py", "Login"),
            ]
        )
        switch_page("Login")
    except KeyError:
        st.sidebar.error("Erro no logout. Tente novamente.")

def registrar_venda():
    st.header("Registrar Venda")
    data = requests.get('http://127.0.0.1:5000/estoque').json()
    df = pd.DataFrame(data["Estoque"])
    if df.empty:
        st.warning("Não há produtos cadastrados no estoque.")
    else:
        df = df[["Produto", "Quantidade", "Data de Validade", "Fornecedor", "Custo por Unidade", "Preço de Venda"]]
        produtos = []
        for i in range(len(df)):
            produtos.append(df["Produto"][i] + " /// " + df['Data de Validade'][i])
        produto = st.selectbox("Produto + Data de Validade", produtos, index=None, placeholder="Escolha uma opção")
        try:
            index_produto = produtos.index(produto)
            produto = df["Produto"][index_produto]
        except:
            pass

        try:
            data_de_validade_venda = st.date_input("Data de validade   ", format="DD/MM/YYYY", value=df.loc[df['Produto'] == produto]['Data de Validade'].values[0])
        except:
            data_de_validade_venda = st.date_input("Data de validade    ", format="DD/MM/YYYY")
        try:
            fornecedor_venda = st.text_input("Fornecedor   ", value=df.loc[df['Produto'] == produto]['Fornecedor'].values[0])
        except:
            fornecedor_venda = st.text_input("Fornecedor     ")
        try:
            custo_por_unidade_venda = st.number_input("Custo por unidade   ", min_value=0.00,step=0.01, value=df.loc[df['Produto'] == produto]['Custo por Unidade'].values[0], placeholder="Custo por unidade")
        except:
            custo_por_unidade_venda = st.number_input("Custo por unidade    ", min_value=0.00,step=0.01, value=0.00, placeholder="Custo por unidade")
        try:
            preco_venda_venda = st.number_input("Preço de venda   ", min_value=0.00,step=0.01, value=df.loc[df['Produto'] == produto]['Preço de Venda'].values[0], placeholder="Preço de venda")
        except:
            preco_venda_venda = st.number_input("Preço de venda    ", min_value=0.00,step=0.01, value=0.00, placeholder="Preço de venda")
        try:
            notificacao_baixo_estoque_produto_venda = st.number_input("Notificação de baixo estoque   ", min_value=1,step=1, value=df.loc[df['Produto'] == produto]['Notificação de Baixo Estoque'].values[0], placeholder="Notificação de baixo estoque")
        except:
            notificacao_baixo_estoque_produto_venda = st.number_input("Notificação de baixo estoque    ", min_value=1,step=1, value=15, placeholder="Notificação de baixo estoque")
        try:
            quantidade = st.number_input("Quantidade   ", min_value=1,step=1, value=df.loc[df['Produto'] == produto]['Quantidade'].values[0], placeholder="Quantidade")
        except:
            quantidade = st.number_input("Quantidade    ", min_value=1,step=1, value=1, placeholder="Quantidade")
        quantidade_venda = st.number_input("Quantidade Vendida", min_value=1,step=1, value=1, placeholder="Quantidade")
            

        if st.button("Registrar venda"):
            response = requests.post('http://127.0.0.1:5000/vendas', json={'dados_produto': produto, 'fornecedor': fornecedor_venda, 'quantidade': quantidade_venda, 'data_de_validade': str(data_de_validade_venda), 'custo_por_unidade': custo_por_unidade_venda, 'preco_venda': preco_venda_venda, 'data_venda': str(pd.to_datetime('today').date())})
            if response.status_code == 201:
                quantidade_final = int(quantidade) - int(quantidade_venda)
                response = requests.put('http://127.0.0.1:5000/estoque', json={'produto_update':produto, 'data_de_validade_update': str(data_de_validade_venda), 'fornecedor_update': fornecedor_venda, 'custo_por_unidade_update': custo_por_unidade_venda, 'preco_venda_update': preco_venda_venda, 'quantidade_update': quantidade_final, 'notificacao_baixo_estoque_update': int(notificacao_baixo_estoque_produto_venda)})
                if response.status_code == 200:
                    st.success("Venda registrada com sucesso.")
                    sleep(1)
                    switch_page("Vendas")
                else:
                    st.error("Erro no registro da venda. Tente novamente.")
            else:
                st.error("Erro no cadastro. Tente novamente.")


def vendas_realizadas():
    st.header("Vendas Realizadas")
    if st.button("Mostrar vendas realizadas"):
        data = requests.get('http://127.0.0.1:5000/vendas').json()
        df = pd.DataFrame(data["Vendas"])
        if df.empty:
            st.warning("Não há vendas realizadas.")
        else:
            df = df[["Produto", "Quantidade", "Data de Validade", "Fornecedor", "Custo por Unidade", "Preço de Venda", "Data da Venda"]]
            df["Valor Total"] = df["Quantidade"] * df["Preço de Venda"]
            df["Custo total"] = df["Quantidade"] * df["Custo por Unidade"]
            df["Lucro"] = df["Valor Total"] - df["Quantidade"] * df["Custo por Unidade"]
            st.dataframe(df)

def graficos():
    st.header("Gráficos")
    data = requests.get('http://127.0.0.1:5000/vendas').json()
    df = pd.DataFrame(data["Vendas"])
    if df.empty:
        st.warning("Não há vendas realizadas.")
    else:
        df = df[["Produto", "Quantidade", "Data de Validade", "Fornecedor", "Custo por Unidade", "Preço de Venda", "Data da Venda"]]
        df["Valor Total"] = df["Quantidade"] * df["Preço de Venda"]
        df["Custo total"] = df["Quantidade"] * df["Custo por Unidade"]
        df["Lucro"] = df["Valor Total"] - df["Quantidade"] * df["Custo por Unidade"]

        df_receita = df[["Lucro", "Valor Total", "Custo total", "Produto", "Data da Venda"]]
        
        df_receita['Data da Venda'] = pd.to_datetime(df_receita['Data da Venda'], format='%Y-%m-%d')

        df_receita['Ano'] = df_receita['Data da Venda'].dt.year
        df_receita['Mês'] = df_receita['Data da Venda'].dt.month

        df_mensal = df_receita.groupby(['Ano', 'Mês']).agg({'Lucro': 'sum', 'Custo total': 'sum', 'Valor Total': 'sum'}).reset_index()

        df_mensal = df_mensal.rename(columns={'Ano': 'Ano', 'Mês': 'Mês', 'Lucro': 'Lucro Mensal', 'Custo total': 'Custo Total Mensal', 'Valor Total': 'Valor Total Mensal'})

        df_mensal['Data Mensal'] = pd.to_datetime(df_mensal['Ano'].astype(str) + '-' + df_mensal['Mês'].astype(str), format='%Y-%m')
          
        
        # Gráfico de barras com custo total, preço total e lucro por dia
        fig1 = px.bar(df_receita, x="Data da Venda", y=["Lucro", "Valor Total", "Custo total"], title="Lucro, Valor Total e Custo Total por dia (R$)", labels= {"value": "Valor (R$)", "variable": "Tipo de valor"})
        st.plotly_chart(fig1, use_container_width=True)

        col1, col2 = st.columns(2, gap='large')
        with col1:
            # Gráfico de pizza com lucro por produto
            fig2 = px.pie(df, values='Lucro', names='Produto', title='Lucro por produto (R$)')
            st.plotly_chart(fig2, use_container_width=False)
        
        
        with col2:
            # Gráfico de barras com lucro mensal
            fig3 = px.bar(df_mensal, x="Data Mensal", y="Lucro Mensal", title='Lucro mensal (R$)', labels= {"value": "Valor (R$)", "variable": "Tipo de valor"})
            fig3.update_xaxes(
                tickformat="%b - %Y",  # Formato para "Mês - Ano"
                showgrid=True  # Exibe as grades no eixo x
            )
            fig3.update_layout(bargap=0.8)
            st.plotly_chart(fig3, use_container_width=False)

        col1, col2 = st.columns(2, gap='large')
        with col1:
            # Gráfico de barras com valor total mensal
            fig4 = px.bar(df_mensal, x="Data Mensal", y="Valor Total Mensal", title='Valor Total mensal (Dos produtos vendidos) (R$)', labels= {"value": "Valor (R$)", "variable": "Tipo de valor"})
            fig4.update_xaxes(
                tickformat="%b - %Y",  # Formato para "Mês - Ano"
                showgrid=True  # Exibe as grades no eixo x
            )
            fig4.update_layout(bargap=0.8)
            st.plotly_chart(fig4, use_container_width=True)

        with col2:
            # Gráfico de barras com custo total mensal
                fig5 = px.bar(df_mensal, x="Data Mensal", y="Custo Total Mensal", title='Custo Total mensal (Dos produtos vendidos) (R$)', labels= {"value": "Valor (R$)", "variable": "Tipo de valor"})
                fig5.update_xaxes(
                    tickformat="%b - %Y",  # Formato para "Mês - Ano"
                    showgrid=True  # Exibe as grades no eixo x
                )
                fig5.update_layout(bargap=0.8)
                st.plotly_chart(fig5, use_container_width=True)

    

def tabs():
    tab1, tab2, tab3 = st.tabs(["Registrar Venda", "Vendas Realizadas", "Gráficos"])
    with tab1:
        registrar_venda()
    with tab2:
        vendas_realizadas()
    with tab3:
        graficos()

    

if __name__ == '__main__':
    tabs()