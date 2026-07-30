import customtkinter as ctk
from docxtpl import DocxTemplate
from tkinter import messagebox
from datetime import datetime  # <-- Biblioteca importada para pegar a data de hoje

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class FormularioETPCompleto(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Gerador de ETP Completo - Município de Boa Esperança")
        self.geometry("750x850")
        
        self.lista_itens = []
        
        # Área de rolagem para caber todos os itens confortavelmente
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=700, height=800)
        self.scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # --- SEÇÃO 1: CABEÇALHO ---
        self.criar_titulo("1. Informações Identificadoras")
        self.txt_sec1 = self.criar_campo_linha("Secretaria Demandante (Cabeçalho do documento)")
        self.txt_sec2 = self.criar_campo_linha("Secretaria Demandante (Primeira tabela interna)")
        self.txt_objeto = self.criar_campo_linha("Objeto da Contratação")
        
        # NOVO CAMPO: Campo de Data adicionado na interface
        self.txt_data = self.criar_campo_linha("Data do Documento (DD/MM/AAAA)")
        # Deixa a data de hoje já preenchida para poupar tempo
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        self.txt_data.insert(0, data_hoje)
        
        # --- SEÇÃO 2: CORPO DO TEXTO (ITENS 1 A 3) ---
        self.criar_titulo("2. Justificativas e Critérios Iniciais")
        self.txt_necessidade = self.criar_campo_bloco("1- Descrição da necessidade da contratação:")
        self.txt_previsao_pac = self.criar_campo_linha("2- Previsão da contratação no PAC:")
        self.txt_requisitos = self.criar_campo_bloco("3.1- Requisitos da Contratação:")
        self.txt_inicio_servicos = self.criar_campo_linha("3.2- Início da Prestação de Serviços:")
        self.txt_tipo_prestacao = self.criar_campo_linha("3.3- Tipo da Prestação de Serviços:")
        self.txt_fiscalizacao = self.criar_campo_bloco("3.4- Da fiscalização e acompanhamento contratual:")
        self.txt_garantia = self.criar_campo_bloco("3.5- Da garantia e dos níveis de serviço:")
        self.txt_pagamento = self.criar_campo_bloco("3.6- Do pagamento:")
        
        # --- SEÇÃO 3: TABELA DINÂMICA (ITEM 4) ---
        self.criar_titulo("3. Item 4 - Estimativas de Quantidades (Tabela)")
        
        self.item_frame = ctk.CTkFrame(self.scroll_frame)
        self.item_frame.pack(pady=5, fill="x", padx=10)
        
        self.txt_item_num = ctk.CTkEntry(self.item_frame, placeholder_text="Item", width=50)
        self.txt_item_num.grid(row=0, column=0, padx=5, pady=5)
        
        self.txt_item_desc = ctk.CTkEntry(self.item_frame, placeholder_text="Descrição do Produto/Serviço", width=260)
        self.txt_item_desc.grid(row=0, column=1, padx=5, pady=5)
        
        self.txt_item_un = ctk.CTkEntry(self.item_frame, placeholder_text="Unid.", width=60)
        self.txt_item_un.grid(row=0, column=2, padx=5, pady=5)
        
        self.txt_item_qtd = ctk.CTkEntry(self.item_frame, placeholder_text="Quant.", width=60)
        self.txt_item_qtd.grid(row=0, column=3, padx=5, pady=5)
        
        self.btn_add_item = ctk.CTkButton(self.item_frame, text="Adicionar", command=self.adicionar_item, width=90)
        self.btn_add_item.grid(row=0, column=4, padx=5, pady=5)
        
        self.txt_preview_itens = ctk.CTkTextbox(self.scroll_frame, width=640, height=100)
        self.txt_preview_itens.pack(pady=5)
        self.txt_preview_itens.configure(state="disabled")
        
        # --- SEÇÃO 4: ITENS RELEVANTES FINAIS (5 A 13) ---
        self.criar_titulo("4. Estudos, Impactos e Conclusões")
        self.txt_levantamento = self.criar_campo_bloco("5- Levantamento de mercado:")
        self.txt_estimativa_valor = self.criar_campo_linha("6- Estimativa do valor da contratação (Ex: R$ 0,00):")
        self.txt_descricao_solucao = self.criar_campo_bloco("7- Descrição da solução como um todo:")
        self.txt_justificativa_parc = self.criar_campo_bloco("8- Justificativa do parcelamento ou não:")
        self.txt_demonstrativo_res = self.criar_campo_bloco("9- Demonstrativo dos resultados pretendidos:")
        self.txt_providencias = self.criar_campo_bloco("10- Providências a serem adotadas previamente:")
        self.txt_contratacoes_corr = self.criar_campo_bloco("11- Contratações correlatas e/ou interdependentes:")
        self.txt_impactos_amb = self.criar_campo_bloco("12- Descrição de possíveis impactos ambientais:")
        self.txt_conclusao = self.criar_campo_bloco("13- Conclusão:")
        
        # --- BOTÃO GERAR ---
        self.btn_gerar = ctk.CTkButton(self.scroll_frame, text="GERAR DOCUMENTO ETP COMPLETO", font=("Arial", 16, "bold"), fg_color="green", hover_color="darkgreen", command=self.gerar_documento, height=55)
        self.btn_gerar.pack(pady=30, fill="x", padx=10)

    def criar_titulo(self, texto):
        lbl = ctk.CTkLabel(self.scroll_frame, text=texto, font=("Arial", 15, "bold"), text_color="#1f538d")
        lbl.pack(pady=(25, 5), anchor="w", padx=10)

    def criar_campo_linha(self, dica):
        txt = ctk.CTkEntry(self.scroll_frame, placeholder_text=dica, width=640)
        txt.pack(pady=4, padx=10)
        return txt

    def criar_campo_bloco(self, rotulo):
        lbl = ctk.CTkLabel(self.scroll_frame, text=rotulo, font=("Arial", 12, "bold"))
        lbl.pack(anchor="w", padx=10, pady=(6, 2))
        txt = ctk.CTkTextbox(self.scroll_frame, width=640, height=75)
        txt.pack(pady=2, padx=10)
        return txt

    def adicionar_item(self):
        num = self.txt_item_num.get()
        desc = self.txt_item_desc.get()
        un = self.txt_item_un.get()
        qtd = self.txt_item_qtd.get()
        
        if not num or not desc or not un or not qtd:
            messagebox.showwarning("Aviso", "Preencha a linha do item antes de adicionar!")
            return
            
        item_dit = {"item": num, "descricao": desc, "unidade": un, "quantidade": qtd, "total": qtd}
        self.lista_itens.append(item_dit)
        
        self.txt_preview_itens.configure(state="normal")
        self.txt_preview_itens.insert("end", f"Item {num}: {desc} | Un: {un} | Qtd: {qtd}\n")
        self.txt_preview_itens.configure(state="disabled")
        
        self.txt_item_num.delete(0, "end")
        self.txt_item_desc.delete(0, "end")
        self.txt_item_un.delete(0, "end")
        self.txt_item_qtd.delete(0, "end")

    def gerar_documento(self):
        try:
            doc = DocxTemplate("modelo_etp.docx")
            
            context = {
                "secretaria_demandante1": self.txt_sec1.get(),
                "secretaria_demandante2": self.txt_sec2.get(),
                "objeto": self.txt_objeto.get(),
                "data": self.txt_data.get(),  # <-- VINCULAÇÃO DA DATA COM O ARQUIVO WORD
                "descricao_necessidade": self.txt_necessidade.get("0.0", "end-1c"),
                "previsao_pac": self.txt_previsao_pac.get(),
                "requisitos_contratacao": self.txt_requisitos.get("0.0", "end-1c"),
                "inicio_servicos": self.txt_inicio_servicos.get(),
                "tipo_prestacao": self.txt_tipo_prestacao.get(),
                "fiscalizacao_acompanhamento": self.txt_fiscalizacao.get("0.0", "end-1c"),
                "garantie_niveis_servico": self.txt_garantia.get("0.0", "end-1c"),
                "garantia_niveis_servico": self.txt_garantia.get("0.0", "end-1c"),
                "pagamento": self.txt_pagamento.get("0.0", "end-1c"),
                "itens": self.lista_itens,
                "levantamento_mercado": self.txt_levantamento.get("0.0", "end-1c"),
                "estimativa_valor": self.txt_estimativa_valor.get(),
                "descricao_solucao": self.txt_descricao_solucao.get("0.0", "end-1c"),
                "justificativa_parcelamento": self.txt_justificativa_parc.get("0.0", "end-1c"),
                "demonstrativo_resultados": self.txt_demonstrativo_res.get("0.0", "end-1c"),
                "providencias_previas": self.txt_providencias.get("0.0", "end-1c"),
                "contratacoes_correlatas": self.txt_contratacoes_corr.get("0.0", "end-1c"),
                "impactos_ambientais": self.txt_impactos_amb.get("0.0", "end-1c"),
                "conclusao": self.txt_conclusao.get("0.0", "end-1c")
            }
            
            doc.render(context)
            doc.save("ETP_Final_Preenchido.docx")
            
            messagebox.showinfo("Sucesso", "Estudo Técnico Preliminar gerado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar o documento: {e}")

if __name__ == "__main__":
    app = FormularioETPCompleto()
    app.mainloop()
