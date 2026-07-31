import streamlit as st
from docxtpl import DocxTemplate
import io
import os
import zipfile
from datetime import date

# Configuração visual profissional para smartphone
st.set_page_config(page_title="Gerador ETP Oficial", page_icon="📝", layout="centered")

st.markdown("<h2 style='text-align: center; color: #0284c7;'>📝 Preenchedor de ETP Digital BOA ESPERANÇA - MG</h2>", unsafe_allow_html=True)
st.write("Insira as informações abaixo para preencher o modelo oficial de Boa Esperança/MG:")

# --- FORMULÁRIO DIVIDIDO POR SEÇÕES ---
st.subheader("📌 Informações Básicas")
secretaria = st.text_input("Secretaria demandante", value="Diretoria de Trânsito e Sinalização Pública")
objeto = st.text_area("Objeto da Contratação", placeholder="Ex: Aquisição de materiais de sinalização...")

st.subheader("📄 Itens do Formulário")
desc_necessidade = st.text_area("1 - Descrição da necessidade da contratação")
previsao_pac = st.text_area("2 - Previsão da contratação no Plano Anual de Contratações")
requisitos = st.text_area("3.1 - Requisitos da contratação")
inicio_servicos = st.text_area("3.2 - Prazo de implantação e início dos serviços")
tipo_prestacao = st.text_area("3.3 - Da prestação dos serviços")
fiscalizacao = st.text_area("3.4 - Da fiscalização e acompanhamento")
garantia = st.text_area("3.5 - Da garantia e níveis de serviço")
pagamento = st.text_area("3.6 - Do pagamento")
estimativas_quant = st.text_area("4 - Estimativas das quantidades para contratação")

st.subheader("🛒 Tabela de Itens (Demonstração)")
st.info("O robô irá gerar uma linha com os dados abaixo para validar o modelo.")
item_num = st.text_input("Número do Item", "01")
item_desc = st.text_input("Descrição do Item", "Material de Exemplo")
item_unid = st.text_input("Unidade de Medida", "UNID")
item_quant = st.number_input("Quantidade", min_value=1, value=1)
item_total = st.number_input("Total", min_value=1, value=1)

st.subheader("📊 Mercado e Valores")
levantamento = st.text_area("5 - Levantamento de mercado")
estimativa_valor = st.text_area("6 - Estimativa do valor da contratação")
desc_solucao = st.text_area("7 - Descrição da solução como um todo")
justificativa_parc = st.text_area("8 - Justificativa do parcelamento ou não")
demonstrativo_res = st.text_area("9 - Demonstrativo dos resultados pretendidos")
providencias_previas = st.text_area("10 - Providências a serem adotadas previamente")
contratacoes_corr = st.text_area("11 - Contratações correlatas e/ou interdependentes")
impactos_amb = st.text_area("12 - Descrição de possíveis impactos ambientais")
conclusao = st.text_area("13 - Conclusão")

# --- CONSTRUÇÃO DO DICIONÁRIO DE DADOS ---
dados_etp = {
    "secretaria_demandante1": secretaria,
    "secretaria_demandante2": secretaria,
    "objeto": objeto,
    "descricao_necessidade": desc_necessidade,
    "previsao_pac": previsao_pac,
    "requisitos_contratacao": requisitos,
    "inicio_servicos": inicio_servicos,
    "tipo_prestacao": tipo_prestacao,
    "fiscalizacao_acompanhamento": fiscalizacao,
    "garantia_niveis_servico": garantia,
    "pagamento": pagamento,
    "estimativas_contrataçao": estimativas_quant,
    "itens": [
        {
            "item": item_num,
            "descricao": item_desc,
            "unidade": item_unid,
            "quantidade": item_quant,
            "total": item_total
        }
    ],
    "levantamento_mercado": levantamento,
    "estimativa_valor": estimativa_valor,
    "descricao_solucao": desc_solucao,
    "justificativa_parcelamento": justificativa_parc,
    "demonstrativo_resultados": demonstrativo_res,
    "providencias_previas": providencias_previas,
    "contratacoes_correlatas": contratacoes_corr,
    "impactos_ambientais": impacts_amb,
    "conclusao": conclusao,
    "data": date.today().strftime("%d/%m/%Y")
}

st.markdown("---")

def forcar_substituicao_xml(caminho_modelo, texto_substituto):
    """Substitui cirurgicamente a tag no arquivo XML interno do Word bypassando lixos de formatação"""
    with open(caminho_modelo, 'rb') as f:
        orig_bytes = f.read()
        
    in_buf = io.BytesIO(orig_bytes)
    out_buf = io.BytesIO()
    
    # Lista de possíveis quebras e variações que o Word gera em segundo plano para a tag do cabeçalho
    alvos_xml = [
        '{{secretaria_demandante1}}',
        '{{ secretaria_demandante1 }}',
        '{ {secretaria_demandante1} }',
        '{ { secretaria_demandante1 } }'
    ]
    
    with zipfile.ZipFile(in_buf, 'r') as yin:
        with zipfile.ZipFile(out_buf, 'w', zipfile.ZIP_DEFLATED) as yout:
            for item in yin.infolist():
                conteudo = yin.read(item.filename)
                
                # Se for um arquivo de cabeçalho (ex: word/header1.xml, header2.xml)
                if "word/header" in item.filename and ".xml" in item.filename:
                    # Converte o XML para string para fazer o replace de texto puro
                    xml_str = conteudo.decode('utf-8', errors='ignore')
                    
                    # Se achar a tag inteira, substitui
                    substituiu = False
                    for alvo in alvos_xml:
                        if alvo in xml_str:
                            xml_str = xml_str.replace(alvo, texto_substituto)
                            substituiu = True
                            
                    # Se o Word quebrou a tag com marcações XML internas de formatação (Runs)
                    if not substituiu and 'secretaria_demandante1' in xml_str:
                        import re
                        # Expressão regular avançada para limpar marcações XML que dividem as chaves da palavra
                        xml_str = re.sub(r'\{\{\s*<[^>]+>\s*secretaria_demandante1\s*<[^>]+>\s*\}\}', texto_substituto, xml_str)
                        xml_str = re.sub(r'\{\s*<[^>]+>\s*\{\s*<[^>]+>\s*secretaria_demandante1\s*<[^>]+>\s*\}\s*<[^>]+>\s*\}', texto_substituto, xml_str)
                        # Fallback agressivo: se a palavra chave pura estiver lá dentro do cabeçalho isolada
                        xml_str = xml_str.replace('{{secretaria_demandante1}}', texto_substituto)
                    
                    conteudo = xml_str.encode('utf-8')
                
                yout.writestr(item, conteudo)
                
    out_buf.seek(0)
    return out_buf

# --- PROCESSAMENTO DO MODELO ---
if st.button("🚀 GERAR DOCUMENTO ETP OFICIAL"):
    if not objeto or not desc_necessidade:
        st.error("❌ Preencha pelo menos o Objeto e a Descrição da Necessidade para testar.")
    else:
        with st.spinner("Processando ETP na nuvem..."):
            try:
                if not os.path.exists("modelo_etp.docx"):
                    st.error("❌ Erro: O arquivo 'modelo_etp.docx' não foi encontrado no servidor.")
                else:
                    # 1. Aplica a correção de força bruta XML no cabeçalho primeiro
                    buffer_cabecalho_corrigido = forcar_substituicao_xml("modelo_etp.docx", secretaria)
                    
                    # 2. Carrega o documento modificado no DocxTemplate para renderizar o corpo principal normalmente
                    doc = DocxTemplate(buffer_cabecalho_corrigido)
                    doc.render(dados_etp, auto_header_footer=True)
                    
                    # Envia o arquivo finalizado direto para o download do Streamlit
                    buffer = io.BytesIO()
                    doc.save(buffer)
                    buffer.seek(0)
                    
                    st.success("✅ ETP estruturado com sucesso!")
                    
                    st.download_button(
                        label="📥 BAIXAR ETP PREENCHIDO (.DOCX)",
                        data=buffer,
                        file_name=f"ETP_{secretaria[:15]}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"❌ Ocorreu um erro ao processar o documento: {e}")
