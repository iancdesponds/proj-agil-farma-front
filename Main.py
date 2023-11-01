import streamlit as st
import requests
import webbrowser

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

def register():
    st.header("Cadastro de Usuário")
    username = st.text_input("Usuário ")
    if st.button("Cadastrar"):
        response = requests.post('http://localhost:5000/register', data={'username': username})
        if response.status_code == 201:
            st.success("Cadastro realizado com sucesso. Faça o login.")
        else:
            st.error("Erro no cadastro. Tente novamente.")

def login():
    st.header("Login")
    username = st.text_input("Usuário")
    if st.button("Login"):
        response = requests.post('http://localhost:5000/login', data={'username': username})
        if response.status_code == 200:
            st.success("Login bem-sucedido.")
            webbrowser.open("http://localhost:8501/Home")
        else:
            st.error("Usuário não encontrado. Tente novamente.")


def login_register():
    tab1, tab2 = st.tabs(["Login", "Cadastro"])
    with tab1:
        login()
    with tab2:
        register()

if __name__ == '__main__':
    login_register()