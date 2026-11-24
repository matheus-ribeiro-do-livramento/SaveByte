import FreeSimpleGUI as sg
from view.tema_savebyte import (
    configurar_tema,
    cabecalho_savebyte,
    nav_consumidor,
    COR_FUNDO,
    COR_CARD,
    COR_VERDE,
    COR_VERDE_CLARO,
    COR_TEXTO,
    COR_TEXTO_SEC,
)


class TelaPainelImpacto:
    def __init__(self):
        configurar_tema()

    def _criar_card_metrica(self, icone: str, titulo: str, valor: str, subtitulo: str):
        return sg.Frame(
            "",
            [
                [
                    sg.Column(
                        [[sg.Text(icone, font=("Helvetica", 20), background_color=COR_VERDE_CLARO, pad=(10, 8))]],
                        background_color=COR_VERDE_CLARO,
                    ),
                    sg.Column(
                        [
                            [sg.Text(titulo, font=("Helvetica", 9, "bold"), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
                            [sg.Text(valor, font=("Helvetica", 15, "bold"), text_color=COR_VERDE, background_color=COR_CARD)],
                            [sg.Text(subtitulo, font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
                        ],
                        background_color=COR_CARD,
                    ),
                ]
            ],
            background_color=COR_CARD,
            relief=sg.RELIEF_SOLID,
            expand_x=True,
            pad=(4, 6),
        )

    def _criar_card_historico(self, item: dict):
        eco_fmt = f"Economizou R$ {item['economia']:.2f}".replace(".", ",")
        preco_fmt = f"R$ {item['preco_pago']:.2f}".replace(".", ",")
        return sg.Frame(
            "",
            [
                [
                    sg.Column(
                        [
                            [sg.Text(f"{item['estabelecimento']}", font=("Helvetica", 8, "bold"), text_color=COR_VERDE, background_color=COR_CARD)],
                            [sg.Text(item["titulo"], font=("Helvetica", 11, "bold"), text_color=COR_TEXTO, background_color=COR_CARD)],
                        ],
                        background_color=COR_CARD,
                    ),
                    sg.Push(background_color=COR_CARD),
                    sg.Column(
                        [
                            [sg.Text(eco_fmt, font=("Helvetica", 9, "bold"), text_color=COR_VERDE, background_color=COR_CARD)],
                            [sg.Text(f"Pago: {preco_fmt}", font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
                        ],
                        background_color=COR_CARD,
                        element_justification="right",
                    ),
                ]
            ],
            background_color=COR_CARD,
            relief=sg.RELIEF_SOLID,
            expand_x=True,
            pad=(2, 4),
        )

    def mostrar_painel(self, dados: dict):
        economia_fmt = f"R$ {dados['economia_total']:.2f}".replace(".", ",")
        comida_fmt = f"{dados['comida_salva_kg']:.1f} kg".replace(".", ",")

        card_economia = self._criar_card_metrica(
            "R$", "Economia Total", economia_fmt, "em ofertas resgatadas"
        )
        card_resgates = self._criar_card_metrica(
            "#", "Ofertas Resgatadas", str(dados["total_resgates"]), f"≈ {comida_fmt} salvos"
        )

        card_gamificacao = sg.Frame(
            "",
            [
                [
                    sg.Text(font=("Helvetica", 16), background_color=COR_VERDE_CLARO, pad=(8, 4)),
                    sg.Column(
                        [
                            [sg.Text(f"Nível: {dados['nivel']}", font=("Helvetica", 12, "bold"), text_color=COR_TEXTO, background_color=COR_CARD)],
                            [sg.Text(dados["mensagem_progresso"], font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
                        ],
                        background_color=COR_CARD,
                    ),
                ],
                [
                    sg.ProgressBar(
                        max_value=max(1, dados["meta_proximo_nivel"]),
                        orientation="h",
                        size=(38, 12),
                        bar_color=(COR_VERDE, COR_VERDE_CLARO),
                        key="-BARRA_NIVEL-",
                    )
                ],
            ],
            background_color=COR_CARD,
            relief=sg.RELIEF_SOLID,
            expand_x=True,
            pad=(4, 8),
        )

        if dados["historico"]:
            linhas_hist = [[self._criar_card_historico(item)] for item in dados["historico"]]
            bloco_historico = [
                sg.Column(
                    linhas_hist,
                    scrollable=True,
                    vertical_scroll_only=True,
                    size=(420, 150),
                    background_color=COR_FUNDO,
                    pad=(0, 4),
                )
            ]
        else:
            bloco_historico = [
                sg.Frame(
                    "",
                    [[
                        sg.Text(
                            "Você ainda não resgatou nenhuma oferta.\nResgate uma oferta para começar seu impacto!",
                            font=("Helvetica", 9),
                            text_color=COR_TEXTO_SEC,
                            background_color=COR_CARD,
                            justification="center",
                            pad=(16, 18),
                        )
                    ]],
                    background_color=COR_CARD,
                    relief=sg.RELIEF_SOLID,
                    expand_x=True,
                    element_justification="center",
                )
            ]

        layout = [
            *cabecalho_savebyte(
                "Painel de Impacto",
                "Acompanhe sua economia financeira e as ofertas salvas do desperdício.",
            ),
            [card_economia, card_resgates],
            [card_gamificacao],
            [sg.Text("Últimos resgates", font=("Helvetica", 10, "bold"), text_color=COR_TEXTO, background_color=COR_FUNDO, pad=((4, 0), (6, 2)))],
            bloco_historico,
            [sg.Button("← Voltar", key="-VOLTAR-", button_color=(COR_TEXTO_SEC, COR_FUNDO), border_width=0, pad=((0, 0), (8, 0)))],
            nav_consumidor("impacto"),
        ]

        window = sg.Window(
            "SaveByte - Painel de Impacto",
            layout,
            size=(460, 620),
            element_justification="center",
            finalize=True,
        )

        progresso = min(dados["total_resgates"], max(1, dados["meta_proximo_nivel"]))
        window["-BARRA_NIVEL-"].update(progresso)

        evento, _ = window.read()
        window.close()
        return evento