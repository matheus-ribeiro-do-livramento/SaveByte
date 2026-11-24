# view/tela_estabelecimento.py
import FreeSimpleGUI as sg
from view.tema_savebyte import (
    configurar_tema, cabecalho_savebyte, botao_verde, nav_estabelecimento,
    COR_FUNDO, COR_CARD, COR_VERDE, COR_TEXTO, COR_TEXTO_SEC
)

class TelaEstabelecimento:
    def __init__(self):
        configurar_tema()

    def cadastro_ou_login(self):
        layout = [
            *cabecalho_savebyte("Área do Estabelecimento", "Gerencie suas ofertas relâmpago e valide retiradas."),
            [botao_verde("Login de Estabelecimento", "-LOGIN-", size=(34, 2))],
            [botao_verde("Cadastrar Estabelecimento", "-CADASTRO-", size=(34, 2))],
            [sg.Button("← Voltar", key="-VOLTAR-", button_color=(COR_TEXTO_SEC, COR_FUNDO), border_width=0, pad=((0, 0), (14, 0)))]
        ]
        window = sg.Window("SaveByte - Estabelecimento", layout, size=(430, 340), element_justification="center")
        event, _ = window.read()
        window.close()

        mapa = {"-CADASTRO-": 1, "-LOGIN-": 2}
        return mapa.get(event, 0)

    def pegaDadosEstabelecimento(self):
        # Inspirado no formulário do protótipo (4nova.png) com os campos do Estabelecimento
        tipos = ["padaria", "restaurante", "mercado"]
        layout = [
            *cabecalho_savebyte("Cadastrar Estabelecimento", "Cadastre sua loja para publicar sacolas e reduzir perdas."),
            [sg.Text("Nome fantasia", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-NOME-", size=(44, 1))],
            [sg.Text("E-mail comercial", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-EMAIL-", size=(44, 1))],
            [sg.Text("Endereço completo", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-ENDERECO-", size=(44, 1))],
            [sg.Text("Bairro", font=("Helvetica", 9, "bold")), sg.Push(), sg.Text("Cidade", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-BAIRRO-", size=(20, 1)), sg.Push(), sg.Input(key="-CIDADE-", size=(20, 1))],
            [sg.Text("CNPJ (somente números)", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-CNPJ-", size=(44, 1))],
            [sg.Text("Tipo de estabelecimento", font=("Helvetica", 9, "bold"))],
            [sg.Combo(tipos, default_value="padaria", key="-TIPO-", readonly=True, size=(42, 1), background_color=COR_CARD)],
            [sg.Text("Senha de acesso", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-SENHA-", password_char="*", size=(44, 1))],
            [botao_verde("Concluir cadastro", "-SALVAR-", size=(38, 1))],
            [sg.Button("Cancelar", key="-CANCELAR-", button_color=(COR_TEXTO_SEC, COR_FUNDO), border_width=0)]
        ]

        window = sg.Window("SaveByte - Novo Estabelecimento", layout, size=(440, 670))
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-CANCELAR-"):
                window.close()
                return None

            if event == "-SALVAR-":
                dados = {
                    "nome": values["-NOME-"].strip(),
                    "email": values["-EMAIL-"].strip(),
                    "endereco": values["-ENDERECO-"].strip(),
                    "bairro": values["-BAIRRO-"].strip(),
                    "cidade": values["-CIDADE-"].strip(),
                    "cnpj": values["-CNPJ-"].strip(),
                    "tipo": values["-TIPO-"].strip(),
                    "senha": values["-SENHA-"].strip(),
                }
                if all(dados.values()):
                    window.close()
                    return dados
                sg.popup_error("Preencha todos os campos obrigatórios!", title="SaveByte")

    def completar_localizacao(self, nome_fantasia: str, endereco_atual: str = "", bairro_atual: str = "", cidade_atual: str = ""):
        layout = [
            *cabecalho_savebyte(
                "Completar localização",
                f"Informe bairro e cidade de '{nome_fantasia}' para que consumidores próximos vejam suas ofertas."
            ),
            [sg.Text("Endereço", font=("Helvetica", 9, "bold"))],
            [sg.Input(endereco_atual, key="-ENDERECO-", size=(42, 1))],
            [sg.Text("Bairro", font=("Helvetica", 9, "bold"))],
            [sg.Input(bairro_atual, key="-BAIRRO-", size=(42, 1))],
            [sg.Text("Cidade", font=("Helvetica", 9, "bold"))],
            [sg.Input(cidade_atual, key="-CIDADE-", size=(42, 1))],
            [botao_verde("Salvar localização", "-SALVAR-", size=(36, 1))],
        ]
        window = sg.Window("Localização do Estabelecimento", layout, size=(430, 390))
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, None):
                window.close()
                return None
            if event == "-SALVAR-":
                bairro = values["-BAIRRO-"].strip()
                cidade = values["-CIDADE-"].strip()
                endereco = values["-ENDERECO-"].strip() or endereco_atual
                if bairro and cidade:
                    window.close()
                    return {"endereco": endereco, "bairro": bairro, "cidade": cidade}
                sg.popup_error("Informe bairro e cidade para continuar.", title="SaveByte")

    def pegaDadosLogin(self):
        layout = [
            *cabecalho_savebyte("Login Estabelecimento", "Acesse o painel da sua loja."),
            [sg.Text("E-mail", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-EMAIL-", size=(42, 1))],
            [sg.Text("Senha", font=("Helvetica", 9, "bold"))],
            [sg.Input(key="-SENHA-", password_char="*", size=(42, 1))],
            [botao_verde("Entrar no painel", "-ENTRAR-", size=(36, 1))],
            [sg.Button("← Voltar", key="-VOLTAR-", button_color=(COR_TEXTO_SEC, COR_FUNDO), border_width=0)]
        ]
        window = sg.Window("Login Estabelecimento", layout, size=(420, 350))
        event, values = window.read()
        window.close()

        if event == "-ENTRAR-":
            return {"email": values["-EMAIL-"].strip(), "senha": values["-SENHA-"].strip()}
        return {"email": "", "senha": ""}

    def menu_gerenciar_ofertas(self):
        # Inspirado na tela "Cadastro de ofertas" (5nova.png) com ações do ControladorEstabelecimento
        card_acoes = sg.Frame("", [
            [botao_verde("+ Cadastrar nova oferta", "-CRIAR-", size=(34, 2))],
            [sg.Button("📋 Visualizar minhas ofertas", key="-LISTAR-", button_color=(COR_TEXTO, COR_CARD), border_width=1, size=(34, 1), pad=(4, 4))],
            [sg.Button("✏️ Atualizar uma oferta", key="-ATUALIZAR-", button_color=(COR_TEXTO, COR_CARD), border_width=1, size=(34, 1), pad=(4, 4))],
            [sg.Button("🗑️ Excluir uma oferta", key="-EXCLUIR-", button_color=("#DC2626", COR_CARD), border_width=1, size=(34, 1), pad=(4, 4))],
        ], background_color=COR_CARD, relief=sg.RELIEF_SOLID, expand_x=True, pad=(4, 8))

        card_retirada = sg.Frame("", [
            [sg.Text("Validação no balcão", font=("Helvetica", 11, "bold"), background_color=COR_CARD)],
            [sg.Text("Confirme o código de 6 dígitos apresentado pelo cliente.", font=("Helvetica", 8), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
            [botao_verde("🚲 Validar resgate de reserva", "-VALIDAR-", size=(34, 1))]
        ], background_color=COR_CARD, relief=sg.RELIEF_SOLID, expand_x=True, pad=(4, 8))

        layout = [
            *cabecalho_savebyte("Cadastro de ofertas", "Gerencie as ofertas ativas e cadastre novas ofertas para resgate."),
            [card_acoes],
            [card_retirada],
            [sg.Button("Sair da conta", key="-SAIR-", button_color=(COR_TEXTO_SEC, COR_FUNDO), border_width=0, pad=((0, 0), (8, 0)))],
            nav_estabelecimento("ofertas")
        ]

        window = sg.Window("SaveByte - Painel do Estabelecimento", layout, size=(440, 580))
        event, _ = window.read()
        window.close()

        # Mantém exata compatibilidade com o dicionário opcoes_oferta do ControladorEstabelecimento
        mapa_opcoes = {
            "-CRIAR-": 1,
            "-LISTAR-": 2,
            "-ATUALIZAR-": 3,
            "-EXCLUIR-": 4,
            "-VALIDAR-": 5,
            "-NAV_RETIRADA-": 5,  # Clicar na aba "Retirada" da barra inferior também abre a validação!
            "-NAV_PERFIL_EST-": 6,
            "-NAV_OFERTAS-": 7,
        }
        return mapa_opcoes.get(event, 0)

    def perfil_estabelecimento(self, estabelecimento):
        tipos = ["padaria", "restaurante", "mercado"]
        tipo_atual = (
            estabelecimento.tipo.value
            if hasattr(estabelecimento.tipo, "value")
            else str(estabelecimento.tipo)
        )
        if tipo_atual not in tipos:
            tipo_atual = "padaria"

        card_identidade = sg.Frame("", [
            [sg.Text("🏪", font=("Helvetica", 24), background_color=COR_CARD)],
            [sg.Text(estabelecimento.nome_fantasia or "", font=("Helvetica", 14, "bold"), text_color=COR_TEXTO, background_color=COR_CARD)],
            [sg.Text(f"CNPJ: {estabelecimento.cnpj} • {estabelecimento.email}", font=("Helvetica", 9), text_color=COR_TEXTO_SEC, background_color=COR_CARD)],
        ], background_color=COR_CARD, relief=sg.RELIEF_SOLID, expand_x=True, pad=(4, 6))

        campos_scroll = [
            [card_identidade],
            [sg.Text("Nome fantasia", font=("Helvetica", 9, "bold"))],
            [sg.Input(estabelecimento.nome_fantasia or "", key="-NOME-", size=(42, 1))],
            [sg.Text("CNPJ (não alterável)", font=("Helvetica", 9, "bold"))],
            [sg.Input(
                str(estabelecimento.cnpj or ""),
                key="-CNPJ-",
                size=(42, 1),
                disabled=True,
                disabled_readonly_background_color="#F3F4F6",
                disabled_readonly_text_color=COR_TEXTO_SEC,
            )],
            [sg.Text("E-mail comercial (não alterável)", font=("Helvetica", 9, "bold"))],
            [sg.Input(
                estabelecimento.email or "",
                key="-EMAIL-",
                size=(42, 1),
                disabled=True,
                disabled_readonly_background_color="#F3F4F6",
                disabled_readonly_text_color=COR_TEXTO_SEC,
            )],
            [sg.Text("Tipo de estabelecimento", font=("Helvetica", 9, "bold"))],
            [sg.Combo(tipos, default_value=tipo_atual, key="-TIPO-", readonly=True, size=(40, 1), background_color=COR_CARD)],
            [sg.Text("Endereço completo", font=("Helvetica", 9, "bold"))],
            [sg.Input(estabelecimento.endereco or "", key="-ENDERECO-", size=(42, 1))],
            [sg.Text("Bairro", font=("Helvetica", 9, "bold")), sg.Push(), sg.Text("Cidade", font=("Helvetica", 9, "bold"))],
            [sg.Input(estabelecimento.bairro or "", key="-BAIRRO-", size=(19, 1)), sg.Push(), sg.Input(estabelecimento.cidade or "", key="-CIDADE-", size=(19, 1))],
            [sg.Text("Ao alterar o endereço, as ofertas ativas serão atualizadas automaticamente.", font=("Helvetica", 8), text_color=COR_TEXTO_SEC)],
            [sg.HorizontalSeparator(pad=((0, 0), (8, 8)))],
            [sg.Text("Alterar senha (opcional)", font=("Helvetica", 10, "bold"), text_color=COR_TEXTO)],
            [sg.Text("Deixe os campos abaixo em branco para manter a senha atual.", font=("Helvetica", 8), text_color=COR_TEXTO_SEC)],
            [sg.Text("Senha atual", font=("Helvetica", 9, "bold"))],
            [sg.Input("", key="-SENHA_ATUAL-", password_char="*", size=(42, 1))],
            [sg.Text("Nova senha", font=("Helvetica", 9, "bold"))],
            [sg.Input("", key="-NOVA_SENHA-", password_char="*", size=(42, 1))],
            [sg.Text("Confirmar nova senha", font=("Helvetica", 9, "bold"))],
            [sg.Input("", key="-CONFIRMAR_SENHA-", password_char="*", size=(42, 1))],
            [botao_verde("Salvar alterações", "-SALVAR-", size=(38, 1))],
        ]

        layout = [
            *cabecalho_savebyte("Meu perfil", "Gerencie os dados cadastrais e a localização do seu estabelecimento."),
            [sg.Column(campos_scroll, scrollable=True, vertical_scroll_only=True, size=(420, 440), background_color=COR_FUNDO)],
            [sg.Button("← Voltar ao menu", key="-VOLTAR-", button_color=(COR_TEXTO_SEC, COR_FUNDO), border_width=0)],
            nav_estabelecimento("perfil"),
        ]

        window = sg.Window("SaveByte - Meu Perfil", layout, size=(460, 700))
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "-VOLTAR-", "-NAV_OFERTAS-"):
                window.close()
                return "ofertas"
            if event == "-NAV_RETIRADA-":
                window.close()
                return "retirada"
            if event == "-NAV_PERFIL_EST-":
                continue
            if event == "-SALVAR-":
                dados = {
                    "nome_fantasia": values["-NOME-"].strip(),
                    "tipo": values["-TIPO-"].strip(),
                    "endereco": values["-ENDERECO-"].strip(),
                    "bairro": values["-BAIRRO-"].strip(),
                    "cidade": values["-CIDADE-"].strip(),
                    "senha_atual": values["-SENHA_ATUAL-"].strip(),
                    "nova_senha": values["-NOVA_SENHA-"].strip(),
                    "confirmar_senha": values["-CONFIRMAR_SENHA-"].strip(),
                }
                if all(dados[campo] for campo in ("nome_fantasia", "tipo", "endereco", "bairro", "cidade")):
                    window.close()
                    return {"acao": "editar", "dados": dados}
                sg.popup_error("Nome fantasia, tipo e localização são obrigatórios!", title="SaveByte")

    def mensagem(self, msg):
        sg.popup_ok(msg, title="SaveByte")