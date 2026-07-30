import streamlit as st
import subprocess
import os

# Configuração visual do aplicativo para telas de celular
st.set_page_config(page_title="Robô ETP Digital", page_icon="🤖")

st.markdown("<h2 style='text-align: center; color: #0284c7;'>🤖 Assistente ETP Digital</h2>", unsafe_allow_html=True)
st.write("Insira seus dados abaixo para ativar o robô preenchedor na nuvem:")

# Caixas de texto limpas (os dados somem assim que fechar a aba)
cpf = st.text_input("👤 CPF do GOV.BR")
senha = st.text_input("🔑 Senha do GOV.BR", type="password")
objeto = st.text_area("📝 Descrição do Objeto do ETP")

# Botão direto para ligar o robô
if st.button("🚀 LIGAR PREENCHEDOR AUTOMÁTICO"):
    if not cpf or not senha or not objeto:
        st.error("❌ Por favor, preencha todos os campos antes de continuar.")
    else:
        with st.spinner("O seu robô Python está rodando no servidor... Acompanhe abaixo:"):
            try:
                # Comando que chama o seu arquivo preencher_etp.py real
                comando = f"python preencher_etp.py '{cpf}' '{senha}' '{objeto}'"
                
                # Executa o seu robô em segundo plano e captura o terminal
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                
                # Mostra o progresso do terminal na tela do celular
                if resultado.stdout:
                    st.code(resultado.stdout)
                
                if resultado.returncode == 0:
                    st.success("✅ Robô finalizou o preenchimento com sucesso!")
                    st.balloons()
                else:
                    st.error("❌ O robô parou com um aviso.")
                    if resultado.stderr:
                        st.error(resultado.stderr)
                    
            except Exception as e:
                st.error(f"Erro ao iniciar o processo do robô: {e}")


                st.error(f"Erro no sistema: {erro}")

