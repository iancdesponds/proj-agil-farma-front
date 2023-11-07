import streamlit as st
import requests
import pandas as pd
from json import *
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page
from time import sleep

st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_title="Produtos")


show_pages(
    [
        Page("pages/Menu.py", "Home"),
        Page("pages/Produtos.py", "Produtos"),
        Page("pages/Estoque.py", "Estoque"),
        Page("pages/Vendas.py", "Vendas"),
    ]
)

st.title("Produtos")

def novo_produto():
    st.header("Novo Produto")
    nome_produto = st.text_input("Nome do produto")
    marca_produto = st.text_input("Marca/Laboratório")
    descricao_produto = st.text_input("Descrição do produto")
    quantidade_por_unidade_produto = st.text_input("Quantidade por unidade")
    notificacao_baixo_estoque_produto = st.number_input("Notificação de baixo estoque", min_value=1,step=1, value=15)
    data = {'marca_produto': marca_produto, 'nome_produto': nome_produto, 'descricao_produto': descricao_produto, 'quantidade_por_unidade_produto': quantidade_por_unidade_produto, 'notificacao_baixo_estoque_produto': notificacao_baixo_estoque_produto}
    if st.button("Cadastrar produto"):
        response = requests.post('http://127.0.0.1:5000/produtos', json={'marca_produto': marca_produto, 'nome_produto': nome_produto, 'descricao_produto': descricao_produto, 'quantidade_por_unidade_produto': quantidade_por_unidade_produto, 'notificacao_baixo_estoque_produto': notificacao_baixo_estoque_produto})
        if response.status_code == 201:
            st.success("Cadastro realizado com sucesso.")
            sleep(1)
        elif response.status_code == 400:
            st.error("Informações inválidas, preencha todos os campos corretamente.")
        else:
            st.error("Erro no cadastro. Tente novamente.")


def editar_produto():
    st.header("Editar Produto")

    data = requests.get('http://127.0.0.1:5000/produtos').json()
    df = pd.DataFrame(data["Produtos"])
    if df.empty:
        st.warning("Não há produtos cadastrados.")
    else:
        df = df[['Marca', 'Nome', 'Descrição', 'Quantidade por Unidade', 'Notificação de Baixo Estoque']]
        produto = st.selectbox("Produto", [produto for produto in df['Nome']], index=None, placeholder="Escolha uma opção")

        try:
            marca_produto_update = st.text_input("Marca/Laboratório ", value=df.loc[df['Nome'] == produto]['Marca'].values[0])
        except:
            marca_produto_update = st.text_input("Marca/Laboratório ")
        try:
            descricao_produto_update = st.text_input("Descrição do produto ", value=df.loc[df['Nome'] == produto]['Descrição'].values[0])
        except:
            descricao_produto_update = st.text_input("Descrição do produto ")
        try:
            quantidade_por_unidade_produto_update = st.text_input("Quantidade por unidade ", value=df.loc[df['Nome'] == produto]['Quantidade por Unidade'].values[0])
        except:
            quantidade_por_unidade_produto_update = st.text_input("Quantidade por unidade ")
        try:
            notificacao_baixo_estoque_produto_update = st.number_input("Notificação de baixo estoque ", min_value=1,step=1, value=df.loc[df['Nome'] == produto]['Notificação de Baixo Estoque'].values[0])
        except:
            notificacao_baixo_estoque_produto_update = st.number_input("Notificação de baixo estoque ", min_value=1,step=1, value=15)
        if st.button("Atualizar dados do produto"):
            response = requests.put('http://127.0.0.1:5000/produtos', json={'nome_produto_update':produto, 'marca_produto_update': marca_produto_update, 'descricao_produto_update': descricao_produto_update, 'quantidade_por_unidade_produto_update': quantidade_por_unidade_produto_update, 'notificacao_baixo_estoque_produto_update': notificacao_baixo_estoque_produto_update})
            if response.status_code == 200:
                st.success("Atualização realizada com sucesso.")
                sleep(1)
                switch_page("Produtos")
            elif response.status_code == 400:
                st.error("Informações inválidas, preencha todos os campos corretamente.")
            else:
                st.error("Erro na atualização. Tente novamente.")


def deletar_produto():
    st.header("Deletar Produto")
    data = requests.get('http://127.0.0.1:5000/produtos').json()
    df = pd.DataFrame(data["Produtos"])
    df = df[['Marca', 'Nome', 'Descrição', 'Quantidade por Unidade', 'Notificação de Baixo Estoque']]
    produto_para_deletar = st.selectbox("Produto  ", [produto for produto in df['Nome']], index=None, placeholder="Escolha uma opção")
    if st.button("Deletar produto"):
        response = requests.delete(f'http://127.0.0.1:5000/produtos/{produto_para_deletar}')
        if response.status_code == 200:
            st.success("Produto deletado com sucesso.")
            sleep(1)
            switch_page("Produtos")
        else:
            st.error("Erro na deleção. Tente novamente.")
        

def listar_produtos():
    st.header("Lista de Produtos")

    if st.button("Mostrar produtos cadastrados"):
        data = requests.get('http://127.0.0.1:5000/produtos').json()
        df = pd.DataFrame(data["Produtos"])
        if df.empty:
            st.warning("Não há produtos cadastrados.")
        else:
            df = df[['Marca', 'Nome', 'Descrição', 'Quantidade por Unidade', 'Notificação de Baixo Estoque']]
            st.dataframe(df)

def tabs():
    tab1, tab2, tab3, tab4 = st.tabs(["Novo Produto", "Editar Produto", "Deletar Produto", "Listar Produtos"])
    with tab1:
        novo_produto()
    with tab2:
        editar_produto()
    with tab3:
        deletar_produto()
    with tab4:
        listar_produtos()

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

if __name__ == '__main__':
    tabs()