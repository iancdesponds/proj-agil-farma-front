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
st.title("Menu - Home")

st.header("Bem-vindo ao sistema de controle de estoque e produtos.")

st.write("Qual página deseja acessar?")

st.link_button("Produtos", "http://localhost:8501/Produtos")
st.link_button("Estoque", "http://localhost:8501/Estoque")
st.link_button("Gráficos", "http://localhost:8501/Graficos")