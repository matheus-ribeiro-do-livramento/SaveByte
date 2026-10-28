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

    def listarOferta (self):
        user = self._controlador_sistema.estabelecimento_logado

        oferta = [of for of in self._ofertas if of.nome_estabelecimento == user.nome_fantasia]

        possuiOfertas = self._telaOferta.exibirOfertas(oferta)
        return possuiOfertas, oferta

    def excluirOferta (self):

        possuiOfertas, ofertas = self.listarOferta()

        if not possuiOfertas:
            self._telaOferta.mensagem('O estabelecimento não possui ofertas relâmpago')
            return
        idSelecionado = self._telaOferta.pegaIdOferta()

        ofertaAExcluir = None

        for of in self._ofertas:
            if of.id == idSelecionado:
                ofertaAExcluir = of
                break

        if not ofertaAExcluir:
            self._telaOferta.mensagem('Erro: Oferta não encontrada')
            return

        possuiReserva = self._controlador_sistema.controlador_reservas.verificar_reserva(idSelecionado)

        if possuiReserva:
            self._telaOferta.mensagem('\nErro: não é possui excluir ofertas que já tenham reservas realizadas')
            return

        confirmaçãoExclusão = self._telaOferta.confimarExclusão(ofertaAExcluir)

        if confirmaçãoExclusão == 'S':
            self._ofertas.remove(ofertaAExcluir)
            self._telaOferta.mensagem(F'\nOferta {idSelecionado} excluida com sucesso!')
            return
        else:
            self._telaOferta.mensagem('\nOperação cancelada')
            return

    def atualizarOferta (self):
        possuiOfertas, oferta = self.listarOferta()

        if not possuiOfertas:
            self._telaOferta.mensagem('\nNão existe ofertas cadastradas')
            return

        idOferta = self._telaOferta.pegaIdOferta()
        oferta = None

        for of in self._ofertas:
            if of.id == idOferta:
                oferta = of

        possuiReserva = self._controlador_sistema.controlador_reservas.verificar_reserva(idOferta)

        if possuiReserva:
            self._telaOferta.mensagem('\nOferta já possui reserva')
            return

        ofertaAtualizada = self._telaOferta.exibirCamposOferta(oferta)

        inicio_org = oferta.inicio
        fim_org = oferta.fim

        oferta.titulo = ofertaAtualizada["titulo"]
        oferta.descricao = ofertaAtualizada["desc"]
        oferta.original = ofertaAtualizada["original"]
        oferta.desconto = ofertaAtualizada["desconto"]
        oferta.quantidade = ofertaAtualizada["quantidade"]
        oferta.inicio = ofertaAtualizada["inicio"]
        oferta.fim = ofertaAtualizada["fim"]

        tempoValido = oferta.validarJanelaRetirada()
        if tempoValido:
            self._telaOferta.mensagem('Oferta atualizada com sucesso!')
            return
        else:
            oferta.inicio = inicio_org
            oferta.fim = fim_org
            self._telaOferta.mensagem('Erro: Tempo mínimo de retirada de 02:30')
            return

# Feito por Gabriel