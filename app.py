import streamlit as st
from docx import Document
import io

# Configuração visual elegante adaptada para telas de celular
st.set_page_config(page_title="Gerador de ETP Digital", page_icon="📝")

st.markdown("<h2 style='text-align: center; color: #0284c7;'>📝 Gerador de ETP Digital</h2>", unsafe_allow_html=True)
st.write("Digite as informações abaixo para preencher o seu modelo oficial automaticamente:")

# Caixa de entrada para o usuário digitar o texto do objeto
objeto_input = st.text_area("📝 Descrição do Objeto do ETP", placeholder="Ex: Aquisição de licenças de software...", height=150)

# O processo ocorre de forma instantânea diretamente na memória
if objeto_input:
    try:
        # 1. Abre o seu modelo original que está guardado no GitHub
        if not os.path.exists("modelo_etp.docx"):
            st.error("❌ Erro: O arquivo 'modelo_etp.docx' não foi encontrado no servidor.")
        else:
            doc = Document("modelo_etp.docx")
            
            # 2. Varre o documento e substitui as tags pelo texto digitado
            # (Substitua "{{ objeto }}" pela tag exata que está escrita no seu Word)
            for paragrafo in doc.paragraphs:
                if "{{ objeto }}" in paragrafo.text:
                    paragrafo.text = paragrafo.text.replace("{{ objeto }}", objeto_input)
            
            # Varre tabelas também, caso a tag esteja dentro de uma tabela
            for tabela in doc.tables:
                for linha in tabela.rows:
                    for celula in linha.cells:
                        if "{{ objeto }}" in celula.text:
                            celula.text = celula.text.replace("{{ objeto }}", objeto_input)
            
            # 3. Prepara o arquivo para download sem precisar salvar no servidor
            buffer = io.BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            
            st.success("✅ Documento estruturado com sucesso!")
            
            # 4. CRIA O BOTÃO GRANDE DE DOWNLOAD PARA O CELULAR
            st.download_button(
                label="📥 BAIXAR DOCUMENTO ETP (.DOCX)",
                data=buffer,
                file_name="ETP_Digital_Preenchido.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            st.balloons() # Animação de comemoração na tela do smartphone
            
    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao processar o modelo: {e}")
else:
    st.info("💡 Aguardando digitação para liberar o botão de download.")


