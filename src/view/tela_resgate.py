class TelaResgate:
    def solicitar_token(self) -> str:
        print("\n--- Validação de Resgate ---")
        codigo = input("Digite o token informado pelo consumidor: ")
        return codigo

    def mostra_mensagem(self, mensagem: str) -> None:
        print(f"\n[SISTEMA]: {mensagem}")


# Feito por Augusto
