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
                "fim": fim}
    
    def pegaIdOferta (self):
            print('\nDigite o ID da oferta que deseja selecionar:')
            return int(input())

    def exibirOfertas (self, ofertas):
        print('\n-----Suas Ofertas-----')
        if not ofertas:
            print("Nenhuma oferta encontrada")
            return False

        for of in ofertas:
            print(f'ID: {of.id} | Titulo: {of.titulo} |\n Desconto: R${of.desconto} | Quantidade: {of.quantidade}')
            return True

    from datetime import datetime

    def exibirCamposOferta(self, oferta):
        print('\n----- Campos Atualizáveis -----')
        print('Deixe o campo em branco e pressione Enter para manter o valor atual.\n')

        print(f'Título atual [{oferta.titulo}]:')
        titulo = input().strip()
        if not titulo:
            titulo = oferta.titulo

        print(f'Descrição atual [{oferta.desc}]:')
        desc = input().strip()
        if not desc:
            desc = oferta.desc

        print(f'Preço original atual [R$ {oferta.original}]:')
        preco_org_str = input().strip()
        if not preco_org_str:
            preco_org = oferta.original
        else:
            preco_org = float(preco_org_str)

        print(f'Preço com desconto atual [R$ {oferta.desconto}]:')
        preco_desc_str = input().strip()
        if not preco_desc_str:
            preco_desc = oferta.desconto
        else:
            preco_desc = float(preco_desc_str)

        print(f'Quantidade disponível atual [{oferta.quantidade}]:')
        quantidade_str = input().strip()
        if not quantidade_str:
            quantidade = oferta.quantidade
        else:
            quantidade = int(quantidade_str)

        inicio_formatado = oferta.inicio.strftime("%H:%M")
        print(f'Hora de início atual [{inicio_formatado}] (Formato HH:MM):')
        inicio = input().strip()
        if not inicio:
            inicio = oferta.inicio
        else:
            inicio = datetime.strptime(inicio, "%H:%M")

        fim_formatado = oferta.fim.strftime("%H:%M")
        print(f'Hora limite atual [{fim_formatado}] (Formato HH:MM):')
        fim = input().strip()
        if not fim:
            fim = oferta.fim
        else:
            fim = datetime.strptime(fim, "%H:%M")

        return {
            "titulo": titulo,
            "desc": desc,
            "original": preco_org,
            "desconto": preco_desc,
            "quantidade": quantidade,
            "inicio": inicio,
            "fim": fim
        }    

    def confimarExclusão(self, oferta):
         self.exibirOfertas(oferta)
         print('\nTem certeza da exclusão (S/N):')
         resposta = input().strip.upper()
         return resposta
         
         
    def mensagem (self, msg):
        print(msg)
    