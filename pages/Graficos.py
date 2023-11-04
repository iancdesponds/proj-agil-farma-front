import streamlit as st
import requests
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page
from time import sleep

st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_title="Gráficos")

show_pages(
    [
        Page("pages/Menu.py", "Home"),
        Page("pages/Produtos.py", "Produtos"),
        Page("pages/Estoque.py", "Estoque"),
        Page("pages/Graficos.py", "Gráficos"),
    ]
)

st.title("Gráficos")

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