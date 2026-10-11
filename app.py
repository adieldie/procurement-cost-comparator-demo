import customtkinter as ctk
from core import compare
from tkinter import messagebox, ttk
import json
import os
from pathlib import Path
from datetime import datetime

# Configurações de tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_DARK = "#0a0a14"
BG_CARD = "#12121f"
ACCENT_PRIMARY = "#3498db"
ACCENT_SUCCESS = "#2ecc71"
ACCENT_WARNING = "#f1c40f"
ACCENT_DANGER = "#e74c3c"
FG_WHITE = "#ffffff"
FG_DIM = "#a0a0b5"
FONT_TITLE = ("Inter", 16, "bold")
FONT_NORMAL = ("Inter", 13)
FONT_HIGHLIGHT = ("Inter", 14, "bold")

HISTORICO_FILE = str(Path.home() / ".procurement-demo-history.json")

class ComparadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Compras (Demo offline)")
        self.root.geometry("1000x720")
        self.root.minsize(950, 700)
        self.root.configure(bg=BG_DARK)
        
        # Histórico
        self.historico = self.carregar_historico()

        self._build_ui()
        self.atualizar_tabela_historico()

    def carregar_historico(self):
        if os.path.exists(HISTORICO_FILE):
            try:
                with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [item for item in data if isinstance(item, dict)] if isinstance(data, list) else []
            except (OSError, ValueError):
                return []
        return []

    def salvar_historico_arquivo(self):
        with open(HISTORICO_FILE, "w", encoding="utf-8") as f:
            json.dump(self.historico, f, indent=4)

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self.root, fg_color=BG_CARD, corner_radius=0)
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header, text="⚖️ COMPARADOR DE CUSTOS", font=FONT_TITLE, text_color=ACCENT_PRIMARY).pack(pady=15)

        # Main Layout
        main_frame = ctk.CTkFrame(self.root, fg_color=BG_DARK)
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Left Panel (Inputs)
        input_panel = ctk.CTkFrame(main_frame, fg_color=BG_CARD, corner_radius=10)
        input_panel.pack(side="left", fill="y", expand=False, padx=(0, 10))
        
        # Section: Informações Gerais
        ctk.CTkLabel(input_panel, text="Dados do Produto", font=FONT_HIGHLIGHT).pack(pady=(15, 5), padx=15, anchor="w")
        
        self.ent_produto = ctk.CTkEntry(input_panel, placeholder_text="Nome do Produto (Ex: Produto de exemplo)")
        self.ent_produto.pack(fill="x", padx=15, pady=5)
        
        self.ent_preco_venda = ctk.CTkEntry(input_panel, placeholder_text="Preço de Venda Final (R$)")
        self.ent_preco_venda.pack(fill="x", padx=15, pady=5)

        # Section: Opção A
        ctk.CTkLabel(input_panel, text="Opção A · pontos fictícios (125 = R$ 1)", font=FONT_HIGHLIGHT, text_color=ACCENT_WARNING).pack(pady=(20, 5), padx=15, anchor="w")
        self.ent_custo_option_a = ctk.CTkEntry(input_panel, placeholder_text="Custo Unitário (R$)")
        self.ent_custo_option_a.pack(fill="x", padx=15, pady=5)
        self.ent_pontos_option_a = ctk.CTkEntry(input_panel, placeholder_text="Pontos Ganhos na Caixa/Pack")
        self.ent_pontos_option_a.pack(fill="x", padx=15, pady=5)
        self.ent_qtd_caixa = ctk.CTkEntry(input_panel, placeholder_text="Unidades na Caixa (Ex: 21)")
        self.ent_qtd_caixa.pack(fill="x", padx=15, pady=5)

        # Section: Fornecedor
        ctk.CTkLabel(input_panel, text="Cotação Outro Fornecedor", font=FONT_HIGHLIGHT, text_color="#9b59b6").pack(pady=(20, 5), padx=15, anchor="w")
        self.ent_nome_fornecedor = ctk.CTkEntry(input_panel, placeholder_text="Nome Fornecedor (Opcional)")
        self.ent_nome_fornecedor.pack(fill="x", padx=15, pady=5)
        self.ent_custo_fornecedor = ctk.CTkEntry(input_panel, placeholder_text="Custo Unitário (R$)")
        self.ent_custo_fornecedor.pack(fill="x", padx=15, pady=5)

        # Buttons
        btn_frame = ctk.CTkFrame(input_panel, fg_color="transparent")
        btn_frame.pack(fill="x", pady=25, padx=15)
        
        self.btn_calcular = ctk.CTkButton(btn_frame, text="Calcular", font=FONT_HIGHLIGHT, fg_color=ACCENT_PRIMARY, hover_color="#2980b9", command=self.calcular)
        self.btn_calcular.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_salvar = ctk.CTkButton(btn_frame, text="Salvar", font=FONT_HIGHLIGHT, fg_color=ACCENT_SUCCESS, hover_color="#27ae60", command=self.salvar_cotacao)
        self.btn_salvar.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # Right Panel (Results + History)
        right_panel = ctk.CTkFrame(main_frame, fg_color=BG_DARK)
        right_panel.pack(side="right", fill="both", expand=True)

        # Results Box
        self.res_box = ctk.CTkFrame(right_panel, fg_color=BG_CARD, corner_radius=10, height=200)
        self.res_box.pack(fill="x", pady=(0, 10))
        self.res_box.pack_propagate(False)

        ctk.CTkLabel(self.res_box, text="Resultado da Matemática", font=FONT_HIGHLIGHT).pack(pady=(15, 10))
        self.lbl_resultado_option_a = ctk.CTkLabel(self.res_box, text="Opção A: Aguardando...", wraplength=410, font=FONT_NORMAL, text_color=FG_DIM)
        self.lbl_resultado_option_a.pack(anchor="w", padx=20, pady=2)
        
        self.lbl_resultado_fornecedor = ctk.CTkLabel(self.res_box, text="Fornecedor: Aguardando...", font=FONT_NORMAL, text_color=FG_DIM)
        self.lbl_resultado_fornecedor.pack(anchor="w", padx=20, pady=2)

        self.lbl_veredito = ctk.CTkLabel(self.res_box, text="-", wraplength=410, font=("Inter", 16, "bold"), text_color=ACCENT_SUCCESS)
        self.lbl_veredito.pack(pady=(15, 0))

        # History Table
        hist_frame = ctk.CTkFrame(right_panel, fg_color=BG_CARD, corner_radius=10)
        hist_frame.pack(fill="both", expand=True)
        ctk.CTkLabel(hist_frame, text="Histórico de Cotações", font=FONT_HIGHLIGHT).pack(pady=(15, 5))

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#1a1a2e", foreground=FG_WHITE, fieldbackground="#1a1a2e", font=("Inter", 9), rowheight=25, borderwidth=0)
        style.configure("Treeview.Heading", background="#2a2a4e", foreground=FG_WHITE, font=("Inter", 10, "bold"), borderwidth=0)
        style.map('Treeview', background=[('selected', ACCENT_PRIMARY)])

        cols = ("data", "produto", "option_a", "fornecedor", "melhor")
        self.tree = ttk.Treeview(hist_frame, columns=cols, show="headings")
        self.tree.heading("data", text="Data")
        self.tree.column("data", width=90, anchor="center")
        self.tree.heading("produto", text="Produto")
        self.tree.column("produto", width=150, anchor="w")
        self.tree.heading("option_a", text="Custo Opção A")
        self.tree.column("option_a", width=90, anchor="center")
        self.tree.heading("fornecedor", text="Custo Forn.")
        self.tree.column("fornecedor", width=90, anchor="center")
        self.tree.heading("melhor", text="Vencedor")
        self.tree.column("melhor", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.btn_limpar = ctk.CTkButton(hist_frame, text="🗑️ Limpar Histórico", fg_color="transparent", text_color=ACCENT_DANGER, hover_color="#2c1a1a", width=120, command=self.limpar_historico)
        self.btn_limpar.pack(pady=(0, 10), padx=10, anchor="e")
        
        # Variáveis de estado
        self.estado_atual = None

    def limpar_historico(self):
        if messagebox.askyesno("Limpar Histórico", "Deseja realmente apagar todo o histórico de cotações?"):
            self.historico = []
            self.salvar_historico_arquivo()
            self.atualizar_tabela_historico()

    def calcular(self):
        self.estado_atual = None
        produto = self.ent_produto.get().strip() or "Produto sem nome"
        pvenda = self.ent_preco_venda.get()
        c_option_a = self.ent_custo_option_a.get()
        p_option_a = self.ent_pontos_option_a.get()
        qtd_caixa = self.ent_qtd_caixa.get()
        
        nome_forn = self.ent_nome_fornecedor.get().strip() or "Outro Fornecedor"
        c_forn = self.ent_custo_fornecedor.get()

        if not c_option_a.strip() or not c_forn.strip():
            messagebox.showwarning("Aviso", "Preencha os dois custos para comparar.")
            return

        try:
            result = compare(c_option_a, c_forn, p_option_a.strip() or 0,
                             qtd_caixa.strip() or 1, 125, pvenda.strip() or 0)
        except ValueError as error:
            messagebox.showwarning("Entrada inválida", str(error))
            return
        venda_float = float(pvenda.replace(',', '.')) if pvenda.strip() else 0.0
        c_option_a_float = float(result['cost_a'])
        c_forn_float = float(result['cost_b'])
        pontos_float = float(p_option_a.replace(',', '.')) if p_option_a.strip() else 0.0
        cashback_unitario = float(result['benefit_a'])
        custo_efetivo_option_a = float(result['effective_a'])
        margem_option_a = float(result['margin_a'] or 0)
        margem_forn = float(result['margin_b'] or 0)

        texto_option_a = f"Opção A: Custo Normal: R$ {c_option_a_float:.2f} | Benefício hipotético por unidade: R$ {cashback_unitario:.2f} ➔ CUSTO ESTIMADO: R$ {custo_efetivo_option_a:.2f}"
        if venda_float > 0:
            texto_option_a += f" (Margem: {margem_option_a:.1f}%)"

        texto_forn = f"{nome_forn}: CUSTO ESTIMADO: R$ {c_forn_float:.2f}"
        if venda_float > 0:
            texto_forn += f" (Margem: {margem_forn:.1f}%)"

        self.lbl_resultado_option_a.configure(text=texto_option_a, text_color=FG_WHITE)
        self.lbl_resultado_fornecedor.configure(text=texto_forn, text_color=FG_WHITE)

        if c_option_a_float >= 0 and c_forn_float >= 0:
            if result['winner'] == 'A':
                veredito = f"🏆 MENOR CUSTO: Opção A! (Mais barato R$ {c_forn_float - custo_efetivo_option_a:.2f} por und)"
                cor = ACCENT_WARNING
                vencedor_nome = "Opção A"
            elif result['winner'] == 'B':
                veredito = f"🏆 MENOR CUSTO: {nome_forn.upper()}! (Mais barato R$ {custo_efetivo_option_a - c_forn_float:.2f} por und)"
                cor = "#9b59b6"
                vencedor_nome = nome_forn
            else:
                veredito = "⚖️ EMPATE TÉCNICO!"
                cor = ACCENT_PRIMARY
                vencedor_nome = "Empate"
        self.lbl_veredito.configure(text=veredito, text_color=cor)

        self.estado_atual = {
            "data": datetime.now().strftime("%d/%m %H:%M"),
            "produto": produto,
            "c_option_a": c_option_a_float,
            "p_option_a": pontos_float,
            "custo_real_option_a": custo_efetivo_option_a,
            "nome_forn": nome_forn,
            "c_forn": c_forn_float,
            "venda": venda_float,
            "vencedor": vencedor_nome
        }

    def salvar_cotacao(self):
        if not self.estado_atual:
            messagebox.showwarning("Aviso", "Calcule a cotação primeiro antes de salvar.")
            return
            
        self.historico.insert(0, self.estado_atual)
        self.salvar_historico_arquivo()
        self.atualizar_tabela_historico()
        
        # Limpar estado e campos, exceto o de venda e fornecedor que podem se repetir
        self.estado_atual = None
        self.ent_produto.delete(0, 'end')
        self.ent_custo_option_a.delete(0, 'end')
        self.ent_pontos_option_a.delete(0, 'end')
        self.ent_qtd_caixa.delete(0, 'end')
        self.ent_custo_fornecedor.delete(0, 'end')
        self.lbl_veredito.configure(text="Cotação Salva com Sucesso!", text_color=ACCENT_SUCCESS)

    def atualizar_tabela_historico(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        for c in self.historico[:50]: # Mostra últimos 50
            self.tree.insert("", "end", values=(
                c.get("data", ""),
                c.get("produto", ""),
                f"R$ {c.get('custo_real_option_a', 0):.2f}",
                f"R$ {c.get('c_forn', 0):.2f}",
                c.get("vencedor", "")
            ))

if __name__ == "__main__":
    root = ctk.CTk()
    app = ComparadorApp(root)
    root.mainloop()

