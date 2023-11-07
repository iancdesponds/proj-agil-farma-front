import streamlit as st
import requests
from st_pages import Page, show_pages, add_page_title, hide_pages
from streamlit_extras.switch_page_button import switch_page
from time import sleep

st.set_page_config(initial_sidebar_state="collapsed", page_title="Home")

show_pages(
    [
        Page("pages/Menu.py", "Home"),
        Page("pages/Produtos.py", "Produtos"),
        Page("pages/Estoque.py", "Estoque"),
        Page("pages/Vendas.py", "Vendas"),
    ]
)


st.title("Menu - Home")

st.header("Bem-vindo ao sistema de controle de estoque e produtos.")

st.write("Qual página deseja acessar?")

produtos = st.button("Produtos")
if produtos:
    switch_page("Produtos")
estoque = st.button("Estoque")
if estoque:
    switch_page("Estoque")
graficos = st.button("Vendas")
if graficos:
    switch_page("Vendas")

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
