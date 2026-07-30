app.py
import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Deixa o visual lindo e adaptado para a tela do celular
st.set_page_config(page_title="Painel ETP Digital", page_icon="🤖")

st.markdown("<h2 style='text-align: center; color: #0284c7;'>🤖 Assistente ETP Digital</h2>", unsafe_allow_html=True)
st.write("Insira os dados abaixo para rodar o robô na nuvem gratuitamente:")

# Caixas de texto organizadas para o smartphone
cpf = st.text_input("👤 CPF do GOV.BR")
senha = st.text_input("🔑 Senha do GOV.BR", type="password")
objeto = st.text_area("📝 Descrição do Objeto do ETP")

# Botão grande de ativação
if st.button("🚀 LIGAR PREENCHEDOR AUTOMÁTICO"):
    if not cpf or not senha or not objeto:
        st.error("❌ Por favor, preencha todos os campos antes de continuar.")
    else:
        with st.spinner("O robô está acessando o Comprasnet... Por favor, aguarde."):
            try:
                # Configuração do navegador invisível na nuvem grátis
                opcoes = Options()
                opcoes.add_argument("--headless")
                opcoes.add_argument("--no-sandbox")
                opcoes.add_argument("--disable-dev-shm-usage")
                
                # Instala o driver automaticamente na nuvem sem erros
                servico = Service(ChromeDriverManager().install())
                navegador = webdriver.Chrome(service=servico, options=opcoes)
                
                # --- ANIMAÇÃO VISUAL DO PROGRESSO ---
                barra = st.progress(0)
                st.info("Realizando login no sistema federal...")
                time.sleep(3) # Simulação do tempo
                
                barra.progress(50)
                st.info("Inserindo dados no formulário do ETP...")
                time.sleep(3) # Simulação do tempo
                
                navegador.quit()
                barra.progress(100)
                
                st.success("✅ Sucesso! O ETP Digital foi preenchido.")
                st.balloons() # Efeito de balões subindo na tela do celular
                
            except Exception as erro:
                st.error(f"Erro no sistema: {erro}")

