import FreeSimpleGUI as sg
from view.tema_savebyte import (
    configurar_tema, cabecalho_savebyte, botao_verde, nav_consumidor,
    COR_FUNDO, COR_CARD, COR_VERDE, COR_VERDE_CLARO, COR_TEXTO, COR_TEXTO_SEC
)

COR_ESGOTADA_BG = "#FEF2F2"
COR_ESGOTADA_TXT = "#DC2626"
COR_ESGOTADA_BTN = "#9CA3AF"


class TelaExplorar:
    def __init__(self):
        configurar_tema()

    def _criar_card_oferta(self, item: dict, idx: int):
        esgotada = item["esgotada"]
        icone_bg = COR_ESGOTADA_BG if esgotada else COR_VERDE_CLARO
        icone_txt = "⛔" if esgotada else "🛍️"

        col_icone = sg.Column(
            [[sg.Text(icone_txt, font=("Helvetica", 24), background_color=icone_bg, pad=(14, 18))]],
            background_color=icone_bg,
        )

        local_texto = item["bairro"]
        if item.get("cidade"):
            local_texto = f"{item['bairro']} • {item['cidade']}"

        badge_texto = "ESGOTADA" if esgotada else f"DISPONÍVEL ({item['quantidade']} un.)"
        badge_fg = COR_ESGOTADA_TXT if esgotada else COR_VERDE
        badge_bg = COR_ESGOTADA_BG if esgotada else COR_VERDE_CLARO

        col_info = sg.Column([
            [
                sg.Text(
                    f"🏪 {item['estabelecimento']}",
                    font=("Helvetica", 9, "bold"),
                    text_color=COR_VERDE if not esgotada else COR_TEXTO_SEC,
                    background_color=COR_CARD,
                ),
                sg.Push(background_color=COR_CARD),
                sg.Text(
                    f" {badge_texto} ",
                    font=("Helvetica", 8, "bold"),
                    text_color=badge_fg,
                    background_color=badge_bg,
                ),
            ],
            [sg.Text(
                f"📍 {local_texto}",
                font=("Helvetica", 8),
                text_color=COR_TEXTO_SEC,
                background_color=COR_CARD,
            )],
            [sg.Text(
                f"⏳ {item['tempo_restante']}",
                font=("Helvetica", 8),
                text_color=COR_TEXTO_SEC,
                background_color=COR_CARD,
            )],
            [sg.Text(
                item["titulo"],
                font=("Helvetica", 12, "bold"),
                text_color=COR_TEXTO if not esgotada else COR_TEXTO_SEC,
                background_color=COR_CARD,
            )],
            [sg.Text(
                item["descricao"],
                font=("Helvetica", 8),
                text_color=COR_TEXTO_SEC,
                background_color=COR_CARD,
                size=(32, 2),
            )],
        ], background_color=COR_CARD, expand_x=True)

        preco_orig = f"De R$ {item['original']:.2f}"
        preco_atual = f"R$ {item['desconto']:.2f}"

        if esgotada:
            rodape_esq = sg.Column([
                [sg.Text(preco_orig, font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
                [sg.Text(preco_atual, font=("Helvetica", 12, "bold"), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
                [sg.Text("Sem estoque disponível no momento", font=("Helvetica", 8, "bold"), text_color=COR_ESGOTADA_TXT, background_color=COR_CARD)],
            ], background_color=COR_CARD)
            botao_acao = sg.Button(
                "Esgotada",
                key=f"-ESGOTADA_{idx}-",
                disabled=True,
                button_color=(COR_CARD, COR_ESGOTADA_BTN),
                border_width=0,
                font=("Helvetica", 9, "bold"),
                size=(12, 1),
            )
        else:
            rodape_esq = sg.Column([
                [sg.Text(preco_orig, font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
                [sg.Text(preco_atual, font=("Helvetica", 13, "bold"), text_color=COR_TEXTO, background_color=COR_CARD)],
            ], background_color=COR_CARD)
            botao_acao = sg.Button(
                "Reservar",
                key=f"-RESERVAR_{idx}-",
                button_color=(COR_CARD, COR_VERDE),
                border_width=0,
                font=("Helvetica", 9, "bold"),
                size=(12, 1),
            )

        linhas_card = [
            [col_icone, col_info],
            [rodape_esq, sg.Push(background_color=COR_CARD), botao_acao],
        ]

        return [sg.Frame("", linhas_card, background_color=COR_CARD, relief=sg.RELIEF_SOLID, expand_x=True, pad=(4, 6))]

    def exibir_painel_explorar(self, bairro: str, cidade: str, ofertas_dados: list):
        """
        Exibe a aba Explorar com ofertas do mesmo bairro/cidade do consumidor.
        Retorna uma tupla (acao, indice_oferta_ou_None).
        """
        local_header = f"{bairro} — {cidade}" if cidade else bairro
        subtitulo = (
            f"Ofertas próximas a você em: {local_header}"
            if local_header.strip(" —")
            else "Complete seu bairro e cidade para visualizar ofertas próximas."
        )

        conteudo_scroll = []
        disponiveis = [(i, item) for i, item in enumerate(ofertas_dados) if not item["esgotada"]]
        esgotadas = [(i, item) for i, item in enumerate(ofertas_dados) if item["esgotada"]]

        if not ofertas_dados:
            conteudo_scroll.append([
                sg.Frame("", [
                    [sg.Text("Nenhuma oferta encontrada no seu bairro.", font=("Helvetica", 11, "bold"), background_color=COR_CARD)],
                    [sg.Text(
                        f"Bairro cadastrado: {local_header or 'Não informado'}\n"
                        "Assim que um estabelecimento do seu bairro publicar uma oferta, ela aparecerá aqui.",
                        font=("Helvetica", 9),
                        text_color=COR_TEXTO_SEC,
                        background_color=COR_CARD,
                        size=(42, 4),
                    )],
                ], background_color=COR_CARD, relief=sg.RELIEF_SOLID, expand_x=True, pad=(4, 8))
            ])
        else:
            if disponiveis:
                conteudo_scroll.append([
                    sg.Text(
                        f"Disponíveis agora ({len(disponiveis)})",
                        font=("Helvetica", 12, "bold"),
                        text_color=COR_TEXTO,
                        pad=((2, 0), (4, 6)),
                    )
                ])
                for idx, item in disponiveis:
                    conteudo_scroll.append(self._criar_card_oferta(item, idx))
            else:
                conteudo_scroll.append([
                    sg.Text(
                        "Todas as ofertas do seu bairro estão esgotadas no momento.",
                        font=("Helvetica", 9),
                        text_color=COR_TEXTO_SEC,
                        pad=((2, 0), (4, 6)),
                    )
                ])

            if esgotadas:
                conteudo_scroll.append([
                    sg.Text(
                        f"Esgotadas ({len(esgotadas)})",
                        font=("Helvetica", 12, "bold"),
                        text_color=COR_ESGOTADA_TXT,
                        pad=((2, 0), (14, 6)),
                    )
                ])
                for idx, item in esgotadas:
                    conteudo_scroll.append(self._criar_card_oferta(item, idx))

        layout = [
            *cabecalho_savebyte("Explorar ofertas", subtitulo),
            [
                sg.Push(),
                sg.Button("🔄 Atualizar", key="-ATUALIZAR-", button_color=(COR_VERDE, COR_CARD), border_width=1, font=("Helvetica", 8, "bold")),
                sg.Button("← Menu", key="-VOLTAR-", button_color=(COR_TEXTO_SEC, COR_FUNDO), border_width=0, font=("Helvetica", 8)),
            ],
            [sg.Column(conteudo_scroll, scrollable=True, vertical_scroll_only=True, size=(430, 440), background_color=COR_FUNDO)],
            nav_consumidor("explorar"),
        ]

        window = sg.Window("SaveByte - Explorar Ofertas", layout, size=(470, 690))
        event, _ = window.read()
        window.close()

        if event and event.startswith("-RESERVAR_"):
            idx = int(event.replace("-RESERVAR_", "").replace("-", ""))
            return ("reservar", idx)
        if event in ("-ATUALIZAR-", "-NAV_EXPLORAR-"):
            return ("atualizar", None)
        if event == "-NAV_RESERVAS-":
            return ("reservas", None)
        if event in ("-NAV_IMPACTO-", "-NAV_PERFIL-"):
            return ("em_breve", None)
        return ("voltar", None)

    def mostra_mensagem(self, msg: str):
        sg.popup_ok(msg, title="SaveByte")
