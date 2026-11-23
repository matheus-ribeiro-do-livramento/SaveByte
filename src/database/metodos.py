from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError
try:
    from .conexao import ConexaoMongo
except ImportError:
    from .conexao import ConexaoMongo


class BaseMetodos:
    def __init__(self, nome_colecao: str):
        db = ConexaoMongo()
        self._collection = db.get_collection(nome_colecao)

    def _converter_id(self, id_valor):
        if isinstance(id_valor, ObjectId):
            return id_valor
        try:
            return ObjectId(id_valor)
        except (InvalidId, TypeError):
            return None

    def inserir(self, dados: dict) -> str:
        try:
            resultado = self._collection.insert_one(dados)
            return str(resultado.inserted_id)
        except DuplicateKeyError:
            raise ValueError("Registro duplicado: já existe um documento com esse identificador único.")

    def buscar_por_id(self, id_valor: str) -> dict | None:
        obj_id = self._converter_id(id_valor)
        if not obj_id:
            return None
        return self._collection.find_one({"_id": obj_id})

    def buscar_um(self, filtro: dict) -> dict | None:
        return self._collection.find_one(filtro)

    def listar(self, filtro: dict | None = None) -> list[dict]:
        return list(self._collection.find(filtro or {}))

    def atualizar(self, id_valor: str, novos_dados: dict) -> bool:
        obj_id = self._converter_id(id_valor)
        if not obj_id:
            return False
        resultado = self._collection.update_one(
            {"_id": obj_id},
            {"$set": novos_dados}
        )
        return resultado.matched_count > 0

    def atualizar_varios(self, filtro: dict, novos_dados: dict) -> int:
        resultado = self._collection.update_many(
            filtro,
            {"$set": novos_dados}
        )
        return resultado.modified_count

    def atualizar_por_filtro(self, filtro: dict, novos_dados: dict) -> bool:
        resultado = self._collection.update_one(
            filtro,
            {"$set": novos_dados}
        )
        return resultado.matched_count > 0

    def deletar(self, id_valor: str) -> bool:
        obj_id = self._converter_id(id_valor)
        if not obj_id:
            return False
        resultado = self._collection.delete_one({"_id": obj_id})
        return resultado.deleted_count > 0

    def deletar_por_filtro(self, filtro: dict) -> bool:
        resultado = self._collection.delete_one(filtro)
        return resultado.deleted_count > 0