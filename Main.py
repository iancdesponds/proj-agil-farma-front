import streamlit as st
import requests
import webbrowser
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page 
from time import sleep

st.set_page_config(initial_sidebar_state="collapsed", page_title="Home - Login/Cadastro")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }

    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""",
    unsafe_allow_html=True,
)

show_pages(
    [
        Page("Main.py", "Login"),
        Page("pages/Menu.py", "Menu"),
    ]
)

def register():
    st.header("Cadastro de Usuário")
    username = st.text_input("Usuário ")
    if st.button("Cadastrar"):
        response = requests.post('http://127.0.0.1:5000/register', json={'username': username})
        if response.status_code == 201:
            st.success("Cadastro realizado com sucesso.")
            sleep(1)
            switch_page("Menu")
            if 'username' not in st.session_state:
                st.session_state['username'] = username
        else:
            st.error("Erro no cadastro. Tente novamente.")

def login():
    st.header("Login")
    username = st.text_input("Usuário")
    if st.button("Login"):
        response = requests.post('http://127.0.0.1:5000/login', json={'username': username})
        if response.status_code == 200:
            st.success("Login bem-sucedido.")
            sleep(1)
            switch_page("Menu")
            if 'username' not in st.session_state:
                st.session_state['username'] = username
        else:
            st.error("Usuário não encontrado. Tente novamente.")

def login_register():
    st.title("Home")

    st.header("Bem-vindo ao sistema de controle de estoque e produtos.")

    st.write("Para começar, faça o login ou cadastre-se.")

    tab1, tab2 = st.tabs(["Login", "Cadastro"])
    with tab1:
        login()
    with tab2:
        register()

if __name__ == '__main__':
    login_register()