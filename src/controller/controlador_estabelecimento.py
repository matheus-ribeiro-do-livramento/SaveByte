from view.tela_estabelecimento import TelaEstabelecimento
from model.estabelecimento import Estabelecimento

class controladorEstabelecimento ():

    def __init__(self, controlador_sistema):
        self.__estabelecimentos = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_estabelecimento = TelaEstabelecimento()

    def iniciarCadastro(self):
        dados = self.__tela_estabelecimento.pegaDadosEstabelecimento()

        certo = self.cadastrarEstabelecimento(dados)

        if (certo):
            return self.__tela_estabelecimento.mensagem('Cadastro efetuado com sucesso')
        else:
            return self.__tela_estabelecimento.mensagem('Erro: CNPJ ou E-mail já em uso')
    

    def cadastrarEstabelecimento (self, dados):

        for est in self.__estabelecimentos:
            if est.email == dados["email"] or est.cnpj == dados["cnpj"]:
                return False
        estabelecimento = Estabelecimento(dados["cnpj"],
                                          dados["endereco"], 
                                          dados["nome"], 
                                          dados["tipo"], 
                                          dados["senha"], 
                                          dados["email"])
        
        self.__estabelecimentos.append(estabelecimento)
        return True

    def iniciarLogin(self):
        dados = self.__tela_estabelecimento.pegaDadosLogin()

        estabelecimento_logado = self.realizarLogin(dados)

        if estabelecimento_logado:
            self.__tela_estabelecimento.mensagem(f'\n Login efetuado com sucesso! \n Bem vindo, {estabelecimento_logado.nome}')

            return estabelecimento_logado
        else:
            self.__tela_estabelecimento.mensagem('Erro: e-mail ou senha invalidos')

            return None

    def realizarLogin (self, dados):
        for est in self.__estabelecimentos:
            if est.email == dados["email"] and est.senha == dados["senha"]:
                return est
        return None
        