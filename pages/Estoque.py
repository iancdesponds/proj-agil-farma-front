import streamlit as st
import requests
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page
from time import sleep
import pandas as pd

st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_title="Estoque")

show_pages(
    [
        Page("pages/Menu.py", "Home"),
        Page("pages/Produtos.py", "Produtos"),
        Page("pages/Estoque.py", "Estoque"),
        Page("pages/Vendas.py", "Vendas"),
    ]
)

st.title("Estoque")

def novo_produto():
    st.header("Novo Produto")
    data = requests.get('http://127.0.0.1:5000/produtos').json()
    df = pd.DataFrame(data["Produtos"])
    df = df[['Marca', 'Nome', 'Descrição', 'Quantidade por Unidade', 'Notificação de Baixo Estoque']]
    produto = st.selectbox("Produto", [produto for produto in df['Nome']], index=None, placeholder="Escolha uma opção")

    data_de_validade = st.date_input("Data de validade", format="DD/MM/YYYY")
    fornecedor = st.text_input("Fornecedor")
    custo_por_unidade = st.number_input("Custo por unidade", min_value=0.00,step=0.01, value=0.00, placeholder="Custo por unidade")
    preco_venda = st.number_input("Preço de venda", min_value=0.00,step=0.01, value=0.00, placeholder="Preço de venda")
    quantidade = st.number_input("Quantidade", min_value=1,step=1, value=1, placeholder="Quantidade")

    if st.button("Cadastrar produto no estoque"):
        try:
            notificacao_baixo_estoque_produto = df.loc[df['Nome'] == produto]['Notificação de Baixo Estoque'].values[0]
        except:
            return st.error("Erro no cadastro. Tente novamente.")
        response = requests.post('http://127.0.0.1:5000/estoque', json={'dados_produto': produto, 'data_de_validade': str(data_de_validade), 'fornecedor': fornecedor, 'custo_por_unidade': custo_por_unidade, 'preco_venda': preco_venda, 'quantidade': quantidade, 'notificacao_baixo_estoque': int(notificacao_baixo_estoque_produto)})
        if response.status_code == 201:
            st.success("Cadastro realizado com sucesso.")
            sleep(1)
            switch_page("Estoque")
        elif response.status_code == 400:
            st.error("Informações inválidas, preencha todos os campos corretamente.")
        else:
            st.error("Erro no cadastro. Tente novamente.")


def editar_produto():
    st.header("Editar Produto no Estoque")
    data = requests.get('http://127.0.0.1:5000/estoque').json()
    df = pd.DataFrame(data["Estoque"])
    if df.empty:
        st.warning("Não há produtos cadastrados no estoque.")
    else:
        df = df[["Produto", "Quantidade", "Data de Validade", "Fornecedor", "Custo por Unidade", "Preço de Venda"]]
        produtos = []
        for i in range(len(df)):
            produtos.append(df["Produto"][i] + " /// " + df['Data de Validade'][i])
        produto = st.selectbox("Produto + Data de Validade", produtos, index=None, placeholder="Escolha uma opção")
        try:
            index_produto = produtos.index(produto)
            produto = df["Produto"][index_produto]
        except:
            pass

        try:
            data_de_validade_update = st.date_input("Data de validade", format="DD/MM/YYYY", value=df.loc[df['Produto'] == produto]['Data de Validade'].values[0])
        except:
            data_de_validade_update = st.date_input("Data de validade ", format="DD/MM/YYYY")
        try:
            fornecedor_update = st.text_input("Fornecedor", value=df.loc[df['Produto'] == produto]['Fornecedor'].values[0])
        except:
            fornecedor_update = st.text_input("Fornecedor ")
        try:
            custo_por_unidade_update = st.number_input("Custo por unidade", min_value=0.00,step=0.01, value=df.loc[df['Produto'] == produto]['Custo por Unidade'].values[0], placeholder="Custo por unidade")
        except:
            custo_por_unidade_update = st.number_input("Custo por unidade ", min_value=0.00,step=0.01, value=0.00, placeholder="Custo por unidade")
        try:
            preco_venda_update = st.number_input("Preço de venda", min_value=0.00,step=0.01, value=df.loc[df['Produto'] == produto]['Preço de Venda'].values[0], placeholder="Preço de venda")
        except:
            preco_venda_update = st.number_input("Preço de venda ", min_value=0.00,step=0.01, value=0.00, placeholder="Preço de venda")
        try:
            quantidade_update = st.number_input("Quantidade", min_value=1,step=1, value=df.loc[df['Produto'] == produto]['Quantidade'].values[0], placeholder="Quantidade")
        except:
            quantidade_update = st.number_input("Quantidade ", min_value=1,step=1, value=1, placeholder="Quantidade")
        try:
            notificacao_baixo_estoque_produto_update = st.number_input("Notificação de baixo estoque", min_value=1,step=1, value=df.loc[df['Produto'] == produto]['Notificação de Baixo Estoque'].values[0], placeholder="Notificação de baixo estoque")
        except:
            notificacao_baixo_estoque_produto_update = st.number_input("Notificação de baixo estoque ", min_value=1,step=1, value=15, placeholder="Notificação de baixo estoque")

        if st.button("Atualizar dados do produto"):
            response = requests.put('http://127.0.0.1:5000/estoque', json={'produto_update':produto, 'data_de_validade_update': str(data_de_validade_update), 'fornecedor_update': fornecedor_update, 'custo_por_unidade_update': custo_por_unidade_update, 'preco_venda_update': preco_venda_update, 'quantidade_update': quantidade_update, 'notificacao_baixo_estoque_update': int(notificacao_baixo_estoque_produto_update)})
            if response.status_code == 200:
                st.success("Atualização realizada com sucesso.")
                sleep(1)
                switch_page("Estoque")
            elif response.status_code == 400:
                st.error("Informações inválidas, preencha todos os campos corretamente.")
            else:
                st.error("Erro na atualização. Tente novamente.")

def deletar_produto():
    st.header("Deletar Produto")

    data = requests.get('http://127.0.0.1:5000/estoque').json()
    df = pd.DataFrame(data["Estoque"])
    if df.empty:
        st.warning("Não há produtos cadastrados no estoque.")
    else:
        df = df[["Produto", "Quantidade", "Data de Validade", "Fornecedor", "Custo por Unidade", "Preço de Venda"]]
        produtos = []
        for i in range(len(df)):
            produtos.append(df["Produto"][i] + " /// " + df['Data de Validade'][i])
        produto = st.selectbox("Produto + Data de Validade  ", produtos, index=None, placeholder="Escolha uma opção")
        try:
            index_produto = produtos.index(produto)
            produto = df["Produto"][index_produto]
        except:
            pass
    
        if st.button("Deletar produto"):
            response = requests.delete(f'http://127.0.0.1:5000/estoque/{produto}')
            if response.status_code == 200:
                st.success("Produto deletado com sucesso.")
                sleep(1)
                switch_page("Estoque")
            else:
                st.error("Erro na deleção. Tente novamente.")
    
def listar_produtos():
    st.header("Lista de Estoque")
    if st.button("Mostrar lista de estoque"):
        data = requests.get('http://127.0.0.1:5000/estoque').json()
        df = pd.DataFrame(data["Estoque"])
        if df.empty:
            st.warning("Não há produtos cadastrados no estoque.")
        else:
            df = df[["Produto", "Quantidade", "Data de Validade", "Fornecedor", "Custo por Unidade", "Preço de Venda", "Notificação de Baixo Estoque"]]
            st.dataframe(df)


def produtos_em_baixo_estoque():
    st.header("Produtos em Baixo Estoque")
    if st.button("Mostrar lista de produtos com baixo estoque"):
        data = requests.get('http://127.0.0.1:5000/estoque').json()
        df = pd.DataFrame(data["Estoque"])
        if df.empty:
            st.warning("Não há produtos cadastrados no estoque.")
        else:
            df = df[["Produto", "Quantidade", "Data de Validade", "Fornecedor", "Custo por Unidade", "Preço de Venda", "Notificação de Baixo Estoque"]]
            df = df.loc[df['Quantidade'] <= df['Notificação de Baixo Estoque']]
            st.dataframe(df)

def produtos_proximos_vencimento():
    st.header("Produtos Próximos ao Vencimento")
    if st.button("Mostrar lista de produtos próximos ao vencimento"):
        data = requests.get('http://127.0.0.1:5000/estoque').json()
        df = pd.DataFrame(data["Estoque"])
        if df.empty:
            st.warning("Não há produtos cadastrados no estoque.")
        else:
            df = df[["Produto", "Quantidade", "Data de Validade", "Fornecedor", "Custo por Unidade", "Preço de Venda", "Notificação de Baixo Estoque"]]
            df["Data de Validade"] = pd.to_datetime(df["Data de Validade"])
            df = df.loc[df['Data de Validade'] <= pd.to_datetime('today') + pd.to_timedelta('15D')]
            st.dataframe(df)

def tabs():
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Novo Produto no Estoque", "Editar Produto no Estoque", "Deletar Produto do Estoque", "Listar Produtos em Estoque", "Produtos em Baixo Estoque", "Produtos Próximos ao Vencimento"])
    with tab1:
        novo_produto()
    with tab2:
        editar_produto()
    with tab3:
        deletar_produto()
    with tab4:
        listar_produtos()
    with tab5:
        produtos_em_baixo_estoque()
    with tab6:
        produtos_proximos_vencimento()

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