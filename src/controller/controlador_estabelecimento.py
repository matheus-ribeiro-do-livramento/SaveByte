from view.tela_estabelecimento import TelaEstabelecimento
from model.estabelecimento import Estabelecimento

class ControladorEstabelecimento ():

    def __init__(self, controlador_sistema):
        self.__estabelecimentos = []
        self.__controlador_sistema = controlador_sistema
        self.__tela_estabelecimento = TelaEstabelecimento()
        self._continua = True

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
            self.__tela_estabelecimento.mensagem(f'\n Login efetuado com sucesso! \n Bem vindo, {estabelecimento_logado.nome_fantasia}')
            return estabelecimento_logado
        else:
            self.__tela_estabelecimento.mensagem('Erro: e-mail ou senha invalidos')

            return None

    def retornar(self):
        self._continua = False

    def realizarLogin (self, dados):
        for est in self.__estabelecimentos:
            if est.email == dados["email"] and est.senha == dados["senha"]:
                return est
        return None

    def abre_tela_cadastro_ou_login(self):
        lista_opcoes = {1: self.iniciarCadastro, 
                        2: self.__controlador_sistema.logar_estabelecimento, 
                        0: self.retornar}
        
        self._continua = True
        while self._continua:
            opcao = self.__tela_estabelecimento.cadastro_ou_login()
            if opcao in lista_opcoes:
                lista_opcoes[opcao]()
            else:
                print("Opção inválida")

    def abrir_gerenciador_ofertas(self):
            
            opcoes_oferta = {
                1: self.__controlador_sistema._controlador_oferta.criarOferta,
                2: self.__controlador_sistema._controlador_oferta.listarOferta,
                3: self.__controlador_sistema._controlador_oferta.atualizarOferta,
                4: self.__controlador_sistema._controlador_oferta.excluirOferta
            }
    
            while True:
                opcao = self.__tela_estabelecimento.menu_gerenciar_ofertas()
                if opcao == 0:
                    self._estabelecimento_logado = None 
                    print("\nLogout do estabelecimento efetuado.")
                    break
                elif opcao in opcoes_oferta:
                    opcoes_oferta[opcao]()
                else:
                    print("Opção inválida.")

# Feito por Gabriel
        