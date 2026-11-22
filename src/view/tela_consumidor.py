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
        # Inspirado no layout de inputs da tela "Minha conta" (4nova.png)
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
                [botao_verde("📅 Minhas Reservas", "-RESERVAS-", size=(34, 2))],
                [sg.Button("← Sair da conta", key="-VOLTAR-", button_color=(COR_TEXTO_SEC, "#FAF9F0"), border_width=0, pad=((0, 0), (14, 0)))],
                nav_consumidor("explorar")
            ]
            window = sg.Window("SaveByte - Consumidor", layout, size=(430, 380), element_justification="center")
            event, _ = window.read()
            window.close()

            if event in ("-RESERVAS-", "-NAV_RESERVAS-"):
                return 1
            return 0