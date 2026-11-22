import FreeSimpleGUI as sg

# Paleta do Protótipo SaveByte
COR_FUNDO = "#FAF9F0"        # Creme claro de fundo
COR_CARD = "#FFFFFF"         # Branco dos cards e inputs
COR_VERDE = "#32A864"        # Verde principal dos botões e destaques
COR_VERDE_CLARO = "#E8F8EF"  # Fundo do ícone e box do token
COR_TEXTO = "#111827"        # Texto escuro principal
COR_TEXTO_SEC = "#6B7280"    # Texto cinza descritivo
COR_BORDA = "#E5E7EB"        # Borda sutil
COR_AMARELO = "#FDE047"      # Badge PENDENTE

def configurar_tema():
    sg.theme_background_color(COR_FUNDO)
    sg.theme_element_background_color(COR_FUNDO)
    sg.theme_text_element_background_color(COR_FUNDO)
    sg.theme_text_color(COR_TEXTO)
    sg.theme_input_background_color(COR_CARD)
    sg.theme_input_text_color(COR_TEXTO)
    sg.theme_button_color((COR_CARD, COR_VERDE))
    sg.set_options(font=("Helvetica", 10))

def cabecalho_savebyte(titulo: str, subtitulo: str):
    return [
        [sg.Text("🍃 SAVEBYTE", font=("Helvetica", 11, "bold"), text_color=COR_VERDE, background_color=COR_FUNDO)],
        [sg.Text(titulo, font=("Helvetica", 20, "bold"), text_color=COR_TEXTO, background_color=COR_FUNDO, pad=((0, 0), (4, 2)))],
        [sg.Text(subtitulo, font=("Helvetica", 9), text_color=COR_TEXTO_SEC, background_color=COR_FUNDO, size=(48, 2), pad=((0, 0), (0, 12)))]
    ]

def botao_verde(texto: str, key: str, size=(20, 1)):
    return sg.Button(
        texto,
        key=key,
        button_color=(COR_CARD, COR_VERDE),
        font=("Helvetica", 10, "bold"),
        border_width=0,
        size=size,
        pad=(4, 6)
    )

def botao_secundario(texto: str, key: str, ativo=False):
    cor_bg = COR_VERDE if ativo else COR_CARD
    cor_fg = COR_CARD if ativo else COR_TEXTO_SEC
    return sg.Button(
        texto,
        key=key,
        button_color=(cor_fg, cor_bg),
        font=("Helvetica", 9, "bold" if ativo else "normal"),
        border_width=1,
        pad=(4, 4)
    )

def nav_consumidor(aba_ativa: str):
    abas = [
        ("🧭 Explorar", "-NAV_EXPLORAR-", aba_ativa == "explorar"),
        ("📅 Minhas Reservas", "-NAV_RESERVAS-", aba_ativa == "reservas"),
        ("🌱 Impacto", "-NAV_IMPACTO-", aba_ativa == "impacto"),
        ("👤 Meu Perfil", "-NAV_PERFIL-", aba_ativa == "perfil"),
    ]
    return [sg.Frame("", [[botao_secundario(t, k, a) for t, k, a in abas]], background_color=COR_CARD, relief=sg.RELIEF_SOLID, pad=((0, 0), (14, 4)))]

def nav_estabelecimento(aba_ativa: str):
    abas = [
        ("📅 Minhas ofertas", "-NAV_OFERTAS-", aba_ativa == "ofertas"),
        ("🚲 Retirada", "-NAV_RETIRADA-", aba_ativa == "retirada"),
        ("👤 Meu Perfil", "-NAV_PERFIL_EST-", aba_ativa == "perfil"),
    ]
    return [sg.Frame("", [[botao_secundario(t, k, a) for t, k, a in abas]], background_color=COR_CARD, relief=sg.RELIEF_SOLID, pad=((0, 0), (14, 4)))]