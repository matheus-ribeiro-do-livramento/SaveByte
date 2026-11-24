import FreeSimpleGUI as sg
from view.tema_savebyte import (
    configurar_tema, cabecalho_savebyte, botao_verde, nav_estabelecimento,
    COR_CARD, COR_VERDE, COR_TEXTO, COR_TEXTO_SEC
)

class TelaResgate:
    def __init__(self):
        configurar_tema()

    def solicitar_token(self) -> str:
        # 6 caixas individuais como no protótipo 6nova.png (compatível com secrets.token_hex(3) = 6 chars)
        caixas_codigo = [
            sg.Input(
                "",
                key=f"-DIG_{i}-",
                size=(3, 1),
                font=("Helvetica", 18, "bold"),
                justification="center",
                background_color="#F3F4F6",
                enable_events=True,
                pad=(4, 10)
            )
            for i in range(6)
        ]

        card_instrucoes = sg.Frame("", [
            [sg.Text("1.", font=("Helvetica", 11, "bold"), text_color=COR_VERDE, background_color=COR_CARD),
             sg.Text("Peça o código ao cliente", font=("Helvetica", 11, "bold"), background_color=COR_CARD)],
            [sg.Text("2.", font=("Helvetica", 11, "bold"), text_color=COR_VERDE, background_color=COR_CARD),
             sg.Text("Confira a reserva", font=("Helvetica", 11, "bold"), background_color=COR_CARD)],
        ], background_color=COR_CARD, relief=sg.RELIEF_SOLID, expand_x=True, pad=(4, 8))

        card_codigo = sg.Frame("", [
            [sg.Text("Código da reserva", font=("Helvetica", 13, "bold"), background_color=COR_CARD)],
            [sg.Column([caixas_codigo], justification="center", background_color=COR_CARD)],
            [sg.Column([[botao_verde("Verificar", "-VERIFICAR-", size=(22, 1))]], justification="center", background_color=COR_CARD)]
        ], background_color=COR_CARD, relief=sg.RELIEF_SOLID, expand_x=True, pad=(4, 8))

        layout = [
            *cabecalho_savebyte("Confirmação de entrega", "Solicite o código de 6 dígitos ao cliente e confira a reserva antes de finalizar."),
            [card_instrucoes],
            [card_codigo],
            [sg.Push()],
            nav_estabelecimento("retirada")
        ]

        window = sg.Window("SaveByte - Validar Retirada", layout, size=(440, 560), finalize=True)
        window["-DIG_0-"].set_focus()

        codigo_final = ""
        self.ultima_navegacao = None
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-NAV_OFERTAS-", "-NAV_PERFIL_EST-"):
                self.ultima_navegacao = event
                break

            # Avança o foco automaticamente ao digitar 1 caractere em cada quadrado
            if event and event.startswith("-DIG_"):
                idx = int(event.replace("-DIG_", "").replace("-", ""))
                val = values[event]
                if len(val) > 1:
                    window[event].update(val[-1])
                if len(val) >= 1 and idx < 5:
                    window[f"-DIG_{idx + 1}-"].set_focus()

            if event == "-VERIFICAR-":
                codigo_final = "".join(values[f"-DIG_{i}-"].strip() for i in range(6))
                break

        window.close()
        return codigo_final

    def mostra_mensagem(self, mensagem: str) -> None:
        sg.popup_ok(mensagem, title="SaveByte - Sistema")