# view/tela_consumidor.py (Principais métodos visuais: Login, Cadastro e Perfil como na imagem 4nova.png)
import FreeSimpleGUI as sg
from view.tema_savebyte import (
    configurar_tema, cabecalho_savebyte, botao_verde,
    nav_consumidor, COR_CARD, COR_TEXTO, COR_TEXTO_SEC
)

class TelaConsumidor:
    def __init__(self):
        configurar_tema()

    def cadastro_ou_login(self):
        layout = [
            *cabecalho_savebyte("Área do Consumidor", "Entre na sua conta ou cadastre-se para reservar."),
            [botao_verde("Fazer Login", "-LOGIN-", size=(32, 2))],
            [botao_verde("Criar Conta", "-CADASTRO-", size=(32, 2))],
            [sg.Button("← Voltar", key="-VOLTAR-", border_width=0)]
        ]
        window = sg.Window("SaveByte - Consumidor", layout, size=(420, 330), element_justification="center")
        event, _ = window.read()
        window.close()

        mapa = {"-CADASTRO-": 1, "-LOGIN-": 2}
        return mapa.get(event, 0)

    def login_consumidor(self):
        layout = [
            *cabecalho_savebyte("Entrar", "Acesse sua conta SaveByte."),
            [sg.Text("E-mail", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-EMAIL-", size=(42, 1))],
            [sg.Text("Senha", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-SENHA-", password_char="*", size=(42, 1))],
            [botao_verde("Entrar", "-CONFIRMAR-", size=(36, 1))]
        ]
        window = sg.Window("Login Consumidor", layout, size=(420, 330))
        event, values = window.read()
        window.close()

        if event == "-CONFIRMAR-":
            return {"email": values["-EMAIL-"], "senha": values["-SENHA-"]}
        return {"email": "", "senha": ""}

    def cadastro_consumidor(self):
        campos = [
            ("Nome completo", "-NOME-"),
            ("E-mail", "-EMAIL-"),
            ("Endereço", "-ENDERECO-"),
            ("Bairro", "-BAIRRO-"),
            ("Cidade", "-CIDADE-"),
            ("Senha", "-SENHA-")
        ]
        layout = [*cabecalho_savebyte("Criar conta", "Preencha seus dados para resgatar alimentos com desconto.")]
        for label, key in campos:
            layout.append([sg.Text(label, font=("Helvetica", 9, "bold"))])
            layout.append([sg.Input(key=key, password_char="*" if key == "-SENHA-" else "", size=(44, 1))])
        layout.append([botao_verde("Cadastrar", "-SALVAR-", size=(38, 1))])

        window = sg.Window("Cadastro Consumidor", layout, size=(430, 560))
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, None):
                window.close()
                return None
            if event == "-SALVAR-":
                if all(values[k].strip() for _, k in campos):
                    window.close()
                    return {
                        "nome": values["-NOME-"],
                        "email": values["-EMAIL-"],
                        "endereco": values["-ENDERECO-"],
                        "bairro": values["-BAIRRO-"],
                        "cidade": values["-CIDADE-"],
                        "senha": values["-SENHA-"],
                    }
                sg.popup_error("Todos os campos são obrigatórios!")

    def mensagem(self, msg):
        sg.popup_ok(msg, title="SaveByte")

    def tela_opcoes(self):
        layout = [
            *cabecalho_savebyte("Área do Consumidor", "O que deseja fazer agora?"),
            [botao_verde(" Explorar Ofertas", "-EXPLORAR-", size=(34, 2))],
            [botao_verde(" Minhas Reservas", "-RESERVAS-", size=(34, 2))],
            [botao_verde(" Painel de Impacto", "-IMPACTO-", size=(34, 2))],
            [sg.Button("← Sair da conta", key="-VOLTAR-", button_color=(COR_TEXTO_SEC, "#FAF9F0"), border_width=0, pad=((0, 0), (14, 0)))],
            nav_consumidor("explorar"),
        ]
        window = sg.Window("SaveByte - Consumidor", layout, size=(430, 480), element_justification="center")
        event, _ = window.read()
        window.close()

            if event in ("-RESERVAS-", "-NAV_RESERVAS-"):
                return 1
            if event in ("-EXPLORAR-", "-NAV_EXPLORAR-"):
                return 2
            if event == "-NAV_PERFIL-":
                return 3
            if event == "-NAV_IMPACTO-":
                return 4
            if event == "-IMPACTO-":
                return 4
            return 0

    def perfil_consumidor(self, consumidor):
        localizacao = consumidor.localizacao
        layout = [
            *cabecalho_savebyte("Meu perfil", "Gerencie seus dados pessoais e sua localização."),
            [sg.Frame("", [
                [sg.Text("👤", font=("Helvetica", 24), background_color=COR_CARD)],
                [sg.Text(consumidor.nome, font=("Helvetica", 14, "bold"), text_color=COR_TEXTO, background_color=COR_CARD)],
                [sg.Text(consumidor.email, font=("Helvetica", 9), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
            ], background_color=COR_CARD, relief=sg.RELIEF_SOLID, expand_x=True, pad=(4, 8))],
            [sg.Text("Nome completo", font=("Helvetica", 9, "bold"))],
            [sg.Input(consumidor.nome, key="-NOME-", size=(44, 1))],
            [sg.Text("E-mail", font=("Helvetica", 9, "bold"))],
            [sg.Input(consumidor.email, key="-EMAIL-", size=(44, 1))],
            [sg.Text("Endereço", font=("Helvetica", 9, "bold"))],
            [sg.Input(localizacao.endereco, key="-ENDERECO-", size=(44, 1))],
            [sg.Text("Bairro", font=("Helvetica", 9, "bold")), sg.Push(), sg.Text("Cidade", font=("Helvetica", 9, "bold"))],
            [sg.Input(localizacao.bairro, key="-BAIRRO-", size=(20, 1)), sg.Push(), sg.Input(localizacao.cidade, key="-CIDADE-", size=(20, 1))],
            [sg.Text("Nova senha", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-SENHA-", password_char="*", size=(44, 1), tooltip="Deixe em branco para manter a senha atual")],
            [botao_verde("Salvar alterações", "-SALVAR-", size=(38, 1))],
            [sg.Button("← Voltar ao menu", key="-VOLTAR-", button_color=(COR_TEXTO_SEC, "#FAF9F0"), border_width=0)],
            nav_consumidor("perfil")
        ]

        window = sg.Window("SaveByte - Meu Perfil", layout, size=(450, 700))
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-VOLTAR-"):
                window.close()
                return "menu"
            if event == "-NAV_EXPLORAR-":
                window.close()
                return "explorar"
            if event == "-NAV_RESERVAS-":
                window.close()
                return "reservas"
            if event == "-NAV_IMPACTO-":
                window.close()
                return "impacto"
            if event == "-NAV_PERFIL-":
                continue
            if event == "-SALVAR-":
                dados = {
                    "nome": values["-NOME-"].strip(),
                    "email": values["-EMAIL-"].strip(),
                    "endereco": values["-ENDERECO-"].strip(),
                    "bairro": values["-BAIRRO-"].strip(),
                    "cidade": values["-CIDADE-"].strip(),
                    "senha": values["-SENHA-"].strip(),
                }
                if all(dados[campo] for campo in ("nome", "email", "endereco", "bairro", "cidade")):
                    window.close()
                    return {"acao": "editar", "dados": dados}
                sg.popup_error("Nome, e-mail e localização são obrigatórios!", title="SaveByte")
