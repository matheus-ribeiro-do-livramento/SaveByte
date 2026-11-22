# view/tela_sistema.py
import FreeSimpleGUI as sg
from view.tema_savebyte import configurar_tema, cabecalho_savebyte, botao_verde, COR_FUNDO

class TelaSistema:
    def __init__(self):
        configurar_tema()

    def estabelecimento_ou_consumidor(self):
        layout = [
            *cabecalho_savebyte("Bem-vindo ao SaveByte", "Combata o desperdício e resgate cestas com desconto."),
            [botao_verde("Acessar como Consumidor", "-CONSUMIDOR-", size=(35, 2))],
            [botao_verde("Acessar como Estabelecimento", "-ESTABELECIMENTO-", size=(35, 2))],
            [sg.Button("Sair", key="-SAIR-", button_color=("#6B7280", COR_FUNDO), border_width=0, pad=((0, 0), (15, 0)))]
        ]
        window = sg.Window("SaveByte", layout, size=(420, 340), element_justification="center", finalize=True)
        event, _ = window.read()
        window.close()

        if event == "-CONSUMIDOR-":
            return 1
        elif event == "-ESTABELECIMENTO-":
            return 2
        return 0