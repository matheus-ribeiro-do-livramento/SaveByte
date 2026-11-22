import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class ConexaoMongo:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conectar()
        return cls._instance

    def _conectar(self):
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME", "savebyte")

        if not mongo_uri:
            raise ValueError("Variável MONGO_URI não encontrada no arquivo .env.")

        self._client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000,
            tlsCAFile=certifi.where(),
        )
        self._db = self._client[db_name]

    def get_collection(self, nome_colecao: str):
        return self._db[nome_colecao]

    def testar_conexao(self) -> bool:
        try:
            self._client.admin.command("ping")
            return True
        except (ConnectionFailure, Exception) as e:
            print(f"Erro ao conectar no MongoDB: {e}")
            return False

    def fechar_conexao(self):
        if self._client:
            self._client.close()
            ConexaoMongo._client = None
            ConexaoMongo._db = None
            ConexaoMongo._instance = None


if __name__ == "__main__":
    conexao = ConexaoMongo()
    if conexao.testar_conexao():
        print("Conexão com o MongoDB estabelecida com sucesso!")
    else:
        print("Falha na conexão com o MongoDB.")