from datetime import datetime
class TelaOfertaRelampago():

    def pegaDadosOferta (self):
        print('\nDigite o id:')
        id = int(input())
        print('\nDigite o titulo da oferta')
        titulo = input()
        print('Digite a descrição da oferta \n (Descreva quais os produtos virão)')
        desc = input()
        print('Digite qual seria o preço total dos produtos')
        preco_org = float(input())
        print('\nDigite o preço com desconto (Preço que será vendido)')
        preco_desc = float(input())
        print('Digite quantas ofertas estão disponiveis ')
        quantidade = int(input())
        print('Digite a a hora de inicio para a retirada (Formato de HH:MM ex: 14:00)')
        jan_inc = input()
        inicio = datetime.strptime(jan_inc, "%H:%M")
        print('Digite a hora limite para retirada (Formato de HH:MM ex: 17:00)')
        jan_fim = input()
        fim = datetime.strptime(jan_fim, "%H:%M")

        return {"id": id, 
                "titulo": titulo,
                "desc": desc,
                "original": preco_org,
                "desconto": preco_desc,
                "quantidade": quantidade,
                "inicio": inicio,
                "fim": jan_fim}

    def mensagem (self, msg):
        print(msg)
    