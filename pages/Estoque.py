import streamlit as st
import requests
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page
from time import sleep
import pandas as pd

st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_title="Estoque")

show_pages(
    [
        Page("pages/Menu.py", "Home"),
        Page("pages/Produtos.py", "Produtos"),
        Page("pages/Estoque.py", "Estoque"),
        Page("pages/Graficos.py", "Gráficos"),
    ]
)

st.title("Estoque")

def novo_produto():
    st.header("Novo Produto")
    data = requests.get('http://127.0.0.1:5000/produtos').json()
    df = pd.DataFrame(data["Produtos"])
    df = df[['Marca', 'Nome', 'Descrição', 'Quantidade por Unidade', 'Notificação de Baixo Estoque']]
    produto = st.selectbox("Produto", [produto for produto in df['Nome']], index=None, placeholder="Escolha uma opção")

    data_de_validade = st.date_input("Data de validade", format="DD/MM/YYYY")
    fornecedor = st.text_input("Fornecedor")
    custo_por_unidade = st.number_input("Custo por unidade", min_value=0.00,step=0.01, value=0.00, placeholder="Custo por unidade")
    preco_venda = st.number_input("Preço de venda", min_value=0.00,step=0.01, value=0.00, placeholder="Preço de venda")
    quantidade = st.number_input("Quantidade", min_value=1,step=1, value=1, placeholder="Quantidade")

    if st.button("Cadastrar produto no estoque"):
        response = requests.post('http://127.0.0.1:5000/estoque', json={'dados_produto': produto, 'data_de_validade': str(data_de_validade), 'fornecedor': fornecedor, 'custo_por_unidade': custo_por_unidade, 'preco_venda': preco_venda, 'quantidade': quantidade})
        if response.status_code == 201:
            st.success("Cadastro realizado com sucesso.")
            sleep(1)
            switch_page("Estoque")
        elif response.status_code == 400:
            st.error("Informações inválidas, preencha todos os campos corretamente.")
        else:
            st.error("Erro no cadastro. Tente novamente.")


def editar_produto():
    st.header("Editar Produto")

def deletar_produto():
    st.header("Deletar Produto")

def listar_produtos():
    st.header("Lista de Estoque")
    if st.button("Mostrar lista de estoque"):
        data = requests.get('http://127.0.0.1:5000/estoque').json()
        df = pd.DataFrame(data["Estoque"])
        if df.empty:
            st.warning("Não há produtos cadastrados no estoque.")
        else:
            df = df[["Produto", "Quantidade", "Data de Validade", "Fornecedor", "Custo por Unidade", "Preço de Venda"]]
            st.dataframe(df)


def produtos_em_baixo_estoque():
    st.header("Produtos em Baixo Estoque")

def tabs():
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Novo Produto no Estoque", "Editar Produto no Estoque", "Deletar Produto do Estoque", "Listar Produtos em Estoque", "Produtos em Baixo Estoque"])
    with tab1:
        novo_produto()
    with tab2:
        editar_produto()
    with tab3:
        deletar_produto()
    with tab4:
        listar_produtos()
    with tab5:
        produtos_em_baixo_estoque()

if st.sidebar.button("Logout"):
    try:
        st.sidebar.success("Logout bem-sucedido.")
        sleep(1)
        show_pages(
            [
                Page("pages/Menu.py", "Home"),
                Page("pages/Produtos.py", "Produtos"),
                Page("pages/Estoque.py", "Estoque"),
                Page("pages/Graficos.py", "Gráficos"),
                Page("Main.py", "Login"),
            ]
        )
        switch_page("Login")
    except KeyError:
        st.sidebar.error("Erro no logout. Tente novamente.")

if __name__ == '__main__':
    tabs()