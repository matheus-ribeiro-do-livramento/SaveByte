from pymongo import ASCENDING, DESCENDING
try:
    from .conexao import ConexaoMongo
except ImportError:
    from conexao import ConexaoMongo


def inicializar_banco():
    db = ConexaoMongo()

    db.get_collection("consumidores").create_index(
        [("email", ASCENDING)],
        unique=True
    )

    estabelecimentos = db.get_collection("estabelecimentos")
    estabelecimentos.create_index([("email", ASCENDING)], unique=True)
    estabelecimentos.create_index([("cnpj", ASCENDING)], unique=True)

    ofertas = db.get_collection("ofertas_relampago")
    ofertas.create_index(
        [("localizacao.cidade", ASCENDING), ("localizacao.bairro", ASCENDING), ("status", ASCENDING)]
    )
    ofertas.create_index([("estabelecimento_id", ASCENDING)])

    reservas = db.get_collection("reservas")
    reservas.create_index(
        [("token.codigo", ASCENDING)],
        unique=True,
        sparse=True
    )
    reservas.create_index(
        [("consumidor_id", ASCENDING), ("estabelecimento_id", ASCENDING), ("data_criacao", DESCENDING)]
    )

    db.get_collection("penalidades").create_index(
        [("consumidor_id", ASCENDING), ("data_aplicacao", DESCENDING)]
    )

    print("Índices e coleções inicializados com sucesso!")


if __name__ == "__main__":
    inicializar_banco()