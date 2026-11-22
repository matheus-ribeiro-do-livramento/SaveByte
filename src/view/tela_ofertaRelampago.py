from datetime import datetime
import FreeSimpleGUI as sg
from view.tema_savebyte import (
    configurar_tema, cabecalho_savebyte, botao_verde, nav_estabelecimento,
    COR_FUNDO, COR_CARD, COR_VERDE, COR_VERDE_CLARO, COR_TEXTO, COR_TEXTO_SEC
)

class TelaOfertaRelampago:
    def __init__(self):
        configurar_tema()

    def pegaDadosOferta(self):
        layout = [
            *cabecalho_savebyte("Nova oferta relâmpago", "Preencha os detalhes da sacola para resgate."),
            [sg.Text("ID da Oferta", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-ID-", size=(42, 1))],
            [sg.Text("Título (ex: Sacola de padaria)", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-TITULO-", size=(42, 1))],
            [sg.Text("Descrição dos itens", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-DESC-", size=(42, 1))],
            [sg.Text("Preço original (R$)", font=("Helvetica", 9, "bold")), sg.Push(), sg.Text("Preço com desconto (R$)", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-ORIG-", size=(18, 1)), sg.Push(), sg.Input(key="-DESC_VAL-", size=(18, 1))],
            [sg.Text("Quantidade de sacolas", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-QTD-", size=(42, 1))],
            [sg.Text("Início retirada (HH:MM)", font=("Helvetica", 9, "bold")), sg.Push(), sg.Text("Limite retirada (HH:MM)", font=("Helvetica", 9, "bold"))],
            [sg.Input("14:00", key="-INICIO-", size=(18, 1)), sg.Push(), sg.Input("17:00", key="-FIM-", size=(18, 1))],
            [botao_verde("Salvar oferta", "-SALVAR-", size=(36, 1))]
        ]
        window = sg.Window("Cadastrar Oferta", layout, size=(420, 520))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                window.close()
                return None
            if event == "-SALVAR-":
                try:
                    dados = {
                        "id": int(values["-ID-"]),
                        "titulo": values["-TITULO-"],
                        "descricao": values["-DESC-"],
                        "original": float(values["-ORIG-"].replace(",", ".")),
                        "desconto": float(values["-DESC_VAL-"].replace(",", ".")),
                        "quantidade": int(values["-QTD-"]),
                        "inicio": datetime.strptime(values["-INICIO-"].strip(), "%H:%M"),
                        "fim": datetime.strptime(values["-FIM-"].strip(), "%H:%M"),
                    }
                    window.close()
                    return dados
                except ValueError:
                    sg.popup_error("Verifique os valores numéricos e o formato de hora (HH:MM).")

    def exibirOfertas(self, ofertas):
        """Corrige inclusive o return dentro do loop que havia no código de terminal e exibe em cards."""
        if not ofertas:
            sg.popup_ok("Nenhuma oferta encontrada.", title="Suas Ofertas")
            return False

        cards = []
        for of in ofertas:
            card = sg.Frame("", [
                [
                    sg.Text("🛍️", font=("Helvetica", 22), background_color=COR_VERDE_CLARO, pad=(12, 12)),
                    sg.Column([
                        [sg.Text(f"#{of.id} - {of.titulo}", font=("Helvetica", 11, "bold"), background_color=COR_CARD)],
                        [sg.Text(of.descricao, font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
                        [sg.Text(f"R$ {of.desconto:.2f} (De R$ {of.original:.2f}) • Qtd: {of.quantidade}", font=("Helvetica", 9, "bold"), text_color=COR_VERDE, background_color=COR_CARD)]
                    ], background_color=COR_CARD)
                ]
            ], background_color=COR_CARD, relief=sg.RELIEF_SOLID, expand_x=True, pad=(4, 4))
            cards.append([card])

        layout = [
            *cabecalho_savebyte("Ofertas ativas", "Acompanhe reservas e horários das ofertas em andamento."),
            [sg.Column(cards, scrollable=True, vertical_scroll_only=True, size=(400, 380), background_color=COR_FUNDO)],
            [botao_verde("Fechar", "-FECHAR-", size=(34, 1))]
        ]
        window = sg.Window("Suas Ofertas", layout, size=(430, 540))
        window.read()
        window.close()
        return True

    def pegaIdOferta(self):
        val = sg.popup_get_text("Digite o ID da oferta que deseja selecionar:", title="Selecionar Oferta")
        return int(val) if val and val.isdigit() else -1

    def confimarExclusão(self, oferta):
        resp = sg.popup_yes_no(f"Tem certeza que deseja excluir '{oferta.titulo}' (ID {oferta.id})?", title="Excluir Oferta")
        return "S" if resp == "Yes" else "N"

    def mensagem(self, msg):
        sg.popup_ok(msg, title="SaveByte")