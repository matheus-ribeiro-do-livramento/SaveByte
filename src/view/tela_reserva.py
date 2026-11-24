import FreeSimpleGUI as sg
from view.tema_savebyte import (
    configurar_tema, cabecalho_savebyte, nav_consumidor,
    COR_FUNDO, COR_CARD, COR_VERDE, COR_VERDE_CLARO, COR_TEXTO, COR_TEXTO_SEC
)

class TelaReserva:
    def __init__(self):
        configurar_tema()

    def _criar_card_reserva(self, dados_reserva, pendente=True):
        """Monta um card visual igual ao protótipo 2nova.png"""
        col_icone = sg.Column(
            [[sg.Text("🛍️", font=("Helvetica", 28), background_color=COR_VERDE_CLARO, pad=(18, 22))]],
            background_color=COR_VERDE_CLARO
        )

        horario = dados_reserva["limite_retirada"].strftime("%d/%m • até %H:%M")
        col_info = sg.Column([
            [sg.Text(f"🏪 {dados_reserva['estabelecimento']}", font=("Helvetica", 9, "bold"), text_color=COR_VERDE, background_color=COR_CARD)],
            [sg.Text(f"🕒 {horario}", font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
            [sg.Text(dados_reserva["titulo"], font=("Helvetica", 13, "bold"), text_color=COR_TEXTO, background_color=COR_CARD)],
            [sg.Text(dados_reserva["descricao"], font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_CARD, size=(30, 2))],
        ], background_color=COR_CARD)

        preco_orig = f"De R$ {dados_reserva['preco_original']:.2f}"
        preco_atual = f"R$ {dados_reserva['preco']:.2f}"

        botao_acao = (
            sg.Button("Cancelar", key=f"-CANCELAR_{dados_reserva['id']}-", button_color=("#DC2626", "#FEE2E2"), border_width=0, font=("Helvetica", 9, "bold"))
            if pendente else
            sg.Button(dados_reserva["status"].capitalize(), disabled=True, button_color=(COR_CARD, COR_VERDE), border_width=0)
        )

        linhas_card = [
            [col_icone, col_info],
            [
                sg.Column([
                    [sg.Text(preco_orig, font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
                    [sg.Text(preco_atual, font=("Helvetica", 13, "bold"), text_color=COR_TEXTO, background_color=COR_CARD)],
                ], background_color=COR_CARD),
                sg.Push(background_color=COR_CARD),
                sg.Button("Ver detalhes", key=f"-DETALHES_{dados_reserva['id']}-", button_color=(COR_CARD, COR_VERDE), border_width=0, font=("Helvetica", 9, "bold")),
                botao_acao
            ]
        ]

        # Caixa destacada do Token de Retirada (igual ao card superior do protótipo 2nova.png)
        if pendente:
            box_token = sg.Frame("", [
                [
                    sg.Text(f"Reserva #{dados_reserva['id']}", font=("Helvetica", 9, "bold"), text_color=COR_VERDE, background_color=COR_VERDE_CLARO),
                    sg.Push(background_color=COR_VERDE_CLARO),
                    sg.Text("Confirmada", font=("Helvetica", 9, "bold"), text_color=COR_VERDE, background_color=COR_VERDE_CLARO)
                ],
                [sg.Text("Apresente esse código de retirada na loja:", font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_VERDE_CLARO)],
                [sg.Text(f"Código de retirada:  {dados_reserva['token']}", font=("Helvetica", 12, "bold"), text_color=COR_TEXTO, background_color=COR_VERDE_CLARO)]
            ], background_color=COR_VERDE_CLARO, relief=sg.RELIEF_FLAT, expand_x=True, pad=(4, 6))
            linhas_card.append([box_token])

        return [sg.Frame("", linhas_card, background_color=COR_CARD, relief=sg.RELIEF_SOLID, expand_x=True, pad=(4, 6))]

    def exibir_painel_reservas(self, atuais_dados: list, anteriores_dados: list):
        """
        Exibe toda a tela de Minhas Reservas de uma vez (substituindo o menu de terminal).
        Retorna uma tupla (acao, id_reserva) para o controlador executar.
        """
        conteudo_scroll = []

        if not atuais_dados:
            conteudo_scroll.append([sg.Text("Você não possui reservas atuais.", text_color=COR_TEXTO_SEC)])
        for r in atuais_dados:
            conteudo_scroll.append(self._criar_card_reserva(r, pendente=True))

        conteudo_scroll.append([sg.Text("Reservas anteriores", font=("Helvetica", 14, "bold"), pad=((0, 0), (14, 6)))])

        if not anteriores_dados:
            conteudo_scroll.append([sg.Text("Você não possui reservas anteriores.", text_color=COR_TEXTO_SEC)])
        for r in anteriores_dados:
            conteudo_scroll.append(self._criar_card_reserva(r, pendente=False))

        layout = [
            *cabecalho_savebyte("Minhas reservas", "Acompanhe seus resgates, verifique seu código de retirada e revise compras."),
            [sg.Column(conteudo_scroll, scrollable=True, vertical_scroll_only=True, size=(410, 460), background_color=COR_FUNDO)],
            nav_consumidor("reservas")
        ]

        window = sg.Window("SaveByte - Minhas Reservas", layout, size=(450, 680))
        event, _ = window.read()
        window.close()

        if event and event.startswith("-CANCELAR_"):
            id_res = int(event.replace("-CANCELAR_", "").replace("-", ""))
            return ("cancelar", id_res)
        if event and event.startswith("-DETALHES_"):
            id_res = int(event.replace("-DETALHES_", "").replace("-", ""))
            return ("detalhes", id_res)
        if event == "-NAV_EXPLORAR-":
            return ("explorar", None)
        if event == "-NAV_RESERVAS-":
            return ("atualizar", None)
        if event == "-NAV_IMPACTO-":
            return ("impacto", None)
        if event == "-NAV_PERFIL-":
            return ("em_breve", None)
        return ("voltar", None)

    def mostra_reserva_detalhes(self, dados_reserva):
        texto = (
            f"Reserva #{dados_reserva['id']} ({dados_reserva['status'].upper()})\n"
            f"Token: {dados_reserva['token']}\n\n"
            f"Oferta: {dados_reserva['titulo']}\n"
            f"Descrição: {dados_reserva['descricao']}\n"
            f"Estabelecimento: {dados_reserva['estabelecimento']}\n"
            f"Valor: R$ {dados_reserva['preco']:.2f} (De R$ {dados_reserva['preco_original']:.2f})\n"
            f"Reservado em: {dados_reserva['data_reserva'].strftime('%d/%m/%Y %H:%M')}\n"
            f"Retirar até: {dados_reserva['limite_retirada'].strftime('%d/%m/%Y %H:%M')}"
        )
        sg.popup(texto, title="Detalhes da Reserva", background_color=COR_CARD, text_color=COR_TEXTO)

    def pergunta_cancelamento(self):
        return sg.popup_yes_no("Deseja realmente cancelar esta reserva?", title="Confirmar Cancelamento") == "Yes"

    def mostra_mensagem(self, msg):
        sg.popup_ok(msg, title="SaveByte")