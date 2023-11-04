import streamlit as st
import requests
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page
from time import sleep

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

def editar_produto():
    st.header("Editar Produto")

def deletar_produto():
    st.header("Deletar Produto")

def listar_produtos():
    st.header("Lista de Produtos")

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
                Page("pages/Graficos.py", "Gráficos"),
                Page("Main.py", "Login"),
            ]
        )
        switch_page("Login")
    except KeyError:
        st.sidebar.error("Erro no logout. Tente novamente.")

if __name__ == '__main__':
    tabs()