import streamlit as st
import requests

st.set_page_config(initial_sidebar_state="collapsed")
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

if __name__ == '__main__':
    tabs()