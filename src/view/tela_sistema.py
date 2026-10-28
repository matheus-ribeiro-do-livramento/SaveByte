class TelaSistema:
    def tela_opcoes(self):
        print("\n-------- SaveByte ---------")
        print("Escolha sua opção:")
        print("1 - Minhas Reservas (Consumidor)")
        print("2 - Cadastrar Estabelecimento")
        print("3 - Login de Estabelecimento")
        print("4 - Painel do Estabelecimento Logado")
        print("0 - Finalizar sistema")
        while True:
            try:
                return int(input("Escolha a opção: "))
            except ValueError:
                print("Valor inválido, digite um número inteiro.")

    def menu_gerenciar_ofertas(self):
        print('\n--- Gerenciar Ofertas Relâmpago ---')
        print('1 - Criar nova oferta')
        print('2 - Visualizar minhas ofertas')
        print('3 - Atualizar uma oferta')
        print('4 - Excluir uma oferta')
        print('0 - Deslogar e Voltar ao menu principal')
        while True:
            try:
                return int(input("Escolha a opção: "))
            except ValueError:
                print("Valor inválido, digite um número inteiro.")