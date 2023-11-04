import streamlit as st
import requests
import pandas as pd
from json import *

st.set_page_config(initial_sidebar_state="collapsed", page_title="Produtos", layout="wide")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Produtos")

def novo_produto():
    st.header("Novo Produto")
    marca_produto = st.text_input("Marca/Laboratório")
    nome_produto = st.text_input("Nome do produto")
    descricao_produto = st.text_input("Descrição do produto")
    quantidade_por_unidade_produto = st.text_input("Quantidade por unidade")
    notificacao_baixo_estoque_produto = st.number_input("Notificação de baixo estoque - Dias", min_value=1,step=1, value=15, placeholder="Dias")
    data = {'marca_produto': marca_produto, 'nome_produto': nome_produto, 'descricao_produto': descricao_produto, 'quantidade_por_unidade_produto': quantidade_por_unidade_produto, 'notificacao_baixo_estoque_produto': notificacao_baixo_estoque_produto}
    if st.button("Cadastrar produto"):
        response = requests.post('http://localhost:5000/produtos', data={'marca_produto': marca_produto, 'nome_produto': nome_produto, 'descricao_produto': descricao_produto, 'quantidade_por_unidade_produto': quantidade_por_unidade_produto, 'notificacao_baixo_estoque_produto': notificacao_baixo_estoque_produto})
        if response.status_code == 201:
            st.success("Cadastro realizado com sucesso.")
        elif response.status_code == 400:
            st.error("Informações inválidas, preencha todos os campos corretamente.")
        else:
            st.error("Erro no cadastro. Tente novamente.")


def editar_produto():
    st.header("Editar Produto")

def deletar_produto():
    st.header("Deletar Produto")

def listar_produtos():
    st.header("Lista de Produtos")

    if st.button("Mostrar produtos cadastrados"):
        data = requests.get('http://localhost:5000/produtos').json()
        df = pd.DataFrame(data["Produtos"])
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

if __name__ == '__main__':
    tabs()