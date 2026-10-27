from view.tela_ofertaRelampago import TelaOfertaRelampago
from model.oferta_relampago import OfertaRelampago

class ControladorOfertaRelampago():

    def __init__(self, controlador_sistema):
        self._ofertas = []
        self._telaOferta = TelaOfertaRelampago()
        self._controlador_sistema = controlador_sistema

    def criarOferta (self):
        dados = self._telaOferta.pegaDadosOferta()
        user = self._controlador_sistema.estabelecimento_logado

        oferta = OfertaRelampago(dados["id"],
                                 dados["titulo"],
                                 dados["desc"],
                                 user.nome_fantasia,
                                 dados["original"],
                                 dados["desconto"],
                                 dados["quantidade"],
                                 dados["inicio"],
                                 dados["fim"])
        tempo_valido = oferta.validarJanelaRetirada()

        if tempo_valido:
            self._ofertas.append(oferta)
            self._telaOferta.mensagem('Oferta criada com sucesso!')
        else:
            self._telaOferta.mensagem('Erro: Minimo de 2h 30min de janela de retirada')

        