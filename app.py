import streamlit as st
import subprocess

# Configuração visual direta do aplicativo
st.set_page_config(page_title="Robô ETP Digital", page_icon="🤖")

st.markdown("<h2 style='text-align: center; color: #0284c7;'>🤖 Gerador de ETP Digital</h2>", unsafe_allow_html=True)
st.write("Digite o conteúdo abaixo para gerar o seu Estudo Técnico Preliminar diretamente:")

# O usuário digita APENAS o objeto do documento
objeto = st.text_area("📝 Descrição do Objeto do ETP", placeholder="Ex: Aquisição de licenças de software...")

# Botão direto para rodar o preenchedor
if st.button("🚀 GERAR ETP IMEDIATAMENTE"):
    if not objeto:
        st.error("❌ Por favor, digite a descrição do objeto antes de ligar o robô!")
    else:
        with st.spinner("O robô está trabalhando no portal do Governo Federal..."):
            try:
                # O comando agora envia apenas o objeto para o seu robô preencher_etp.py
                comando = f"python preencher_etp.py '{objeto}'"
                
                # Executa o seu script em segundo plano
                resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
                
                # Mostra o progresso na tela do celular
                if resultado.stdout:
                    st.code(resultado.stdout)
                
                if resultado.returncode == 0:
                    st.success("✅ ETP Digital gerado e preenchido com sucesso!")
                    st.balloons()
                else:
                    st.error("❌ O robô encontrou uma pendência no processamento.")
                    if resultado.stderr:
                        st.error(resultado.stderr)
                    
            except Exception as e:
                st.error(f"Erro ao iniciar o robô: {e}")
