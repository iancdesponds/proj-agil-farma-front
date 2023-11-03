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
st.title("Home")

st.header("Bem-vindo ao sistema de controle de estoque e produtos.")

st.write("Para começar, faça o login ou cadastre-se.")