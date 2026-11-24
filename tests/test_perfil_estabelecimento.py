import copy
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

ROOT_SRC = Path(__file__).resolve().parents[1] / "src"
if str(ROOT_SRC) not in sys.path:
    sys.path.insert(0, str(ROOT_SRC))

from model.consumidor import Consumidor
from model.localizacao import Localizacao
from model.oferta_relampago import OfertaRelampago
from model.reserva import Reserva
from model.enums import StatusOferta, TipoEstabelecimento
from controller.controlador_estabelecimento import ControladorEstabelecimento
from controller.controlador_oferta_relampago import ControladorOfertaRelampago
from controller.controlador_reserva import ControladorReservas


class FakeBaseMetodos:
    def __init__(self, colecao=""):
        self.colecao = colecao
        self.docs = []

    def _matches(self, doc, filtro):
        for chave, valor in filtro.items():
            if chave == "$or":
                if not any(self._matches(doc, sub) for sub in valor):
                    return False
                continue
            partes = chave.split(".")
            atual = doc
            encontrou = True
            for p in partes:
                if isinstance(atual, dict) and p in atual:
                    atual = atual[p]
                else:
                    encontrou = False
                    break
            if not encontrou or atual != valor:
                return False
        return True

    def _aplicar_set(self, doc, novos_dados):
        for chave, valor in novos_dados.items():
            partes = chave.split(".")
            alvo = doc
            for p in partes[:-1]:
                if p not in alvo or not isinstance(alvo[p], dict):
                    alvo[p] = {}
                alvo = alvo[p]
            alvo[partes[-1]] = copy.deepcopy(valor)

    def inserir(self, dados):
        self.docs.append(copy.deepcopy(dados))
        return str(len(self.docs))

    def buscar_um(self, filtro):
        for doc in self.docs:
            if self._matches(doc, filtro):
                return copy.deepcopy(doc)
        return None

    def listar(self, filtro=None):
        if not filtro:
            return [copy.deepcopy(d) for d in self.docs]
        return [copy.deepcopy(d) for d in self.docs if self._matches(d, filtro)]

    def atualizar_por_filtro(self, filtro, novos_dados):
        for doc in self.docs:
            if self._matches(doc, filtro):
                self._aplicar_set(doc, novos_dados)
                return True
        return False

    def atualizar_varios(self, filtro, novos_dados):
        count = 0
        for doc in self.docs:
            if self._matches(doc, filtro):
                self._aplicar_set(doc, novos_dados)
                count += 1
        return count

    def deletar_por_filtro(self, filtro):
        for i, doc in enumerate(self.docs):
            if self._matches(doc, filtro):
                self.docs.pop(i)
                return True
        return False


class FakeSistema:
    def __init__(self):
        self.consumidor_logado = None
        self.estabelecimento_logado = None
        self.controlador_estabelecimento = None
        self.controlador_oferta = None
        self.controlador_reservas = None

    def definir_estabelecimento_logado(self, estabelecimento):
        self.estabelecimento_logado = estabelecimento

    def vincular_estabelecimento(self, estabelecimento, nome_antigo=None):
        if self.controlador_oferta:
            self.controlador_oferta.vincular_estabelecimento_nas_ofertas(estabelecimento, nome_antigo=nome_antigo)
        if self.controlador_reservas:
            self.controlador_reservas.vincular_estabelecimento_nas_reservas(estabelecimento, nome_antigo=nome_antigo)


class TestPerfilEstabelecimento(unittest.TestCase):
    def setUp(self):
        self.sistema = FakeSistema()

        with (
            patch("controller.controlador_estabelecimento.BaseMetodos", FakeBaseMetodos),
            patch("controller.controlador_oferta_relampago.BaseMetodos", FakeBaseMetodos),
            patch("controller.controlador_reserva.BaseMetodos", FakeBaseMetodos),
            patch("controller.controlador_estabelecimento.TelaEstabelecimento"),
            patch("controller.controlador_oferta_relampago.TelaOfertaRelampago"),
            patch("controller.controlador_oferta_relampago.TelaExplorar"),
            patch("controller.controlador_reserva.TelaReserva"),
        ):
            self.ctrl_est = ControladorEstabelecimento(self.sistema)
            self.ctrl_of = ControladorOfertaRelampago(self.sistema)
            self.ctrl_res = ControladorReservas(self.sistema)

        self.sistema.controlador_estabelecimento = self.ctrl_est
        self.sistema.controlador_oferta = self.ctrl_of
        self.sistema.controlador_reservas = self.ctrl_res

        self.assertTrue(self.ctrl_est.cadastrarEstabelecimento({
            "nome": "Padaria Sol",
            "email": "contato@padariasol.com",
            "endereco": "Rua A, 100",
            "bairro": "Centro",
            "cidade": "Florianópolis",
            "cnpj": "12345678000199",
            "tipo": "padaria",
            "senha": "senha123",
        }))
        self.est = self.ctrl_est.realizarLogin({
            "email": "contato@padariasol.com",
            "senha": "senha123",
        })
        self.sistema.definir_estabelecimento_logado(self.est)

    def test_editar_cadastro_e_rn04_ofertas_ativas(self):
        agora = datetime.now()
        oferta_ativa = OfertaRelampago(
            1, "Cesta Manhã", "Pães frescos", self.est.nome_fantasia,
            30.0, 12.0, 5, agora, agora + timedelta(hours=4),
            localizacao=Localizacao("Florianópolis", "Centro", "Rua A, 100"),
        )
        oferta_ativa._estabelecimento_id = self.est.cnpj
        self.ctrl_of._metodos.inserir(self.ctrl_of._oferta_para_documento(oferta_ativa, self.est))
        self.ctrl_of._ofertas.append(oferta_ativa)

        oferta_expirada = OfertaRelampago(
            2, "Cesta Ontem", "Doces", self.est.nome_fantasia,
            25.0, 10.0, 2, agora - timedelta(days=1, hours=4), agora - timedelta(days=1),
            localizacao=Localizacao("Florianópolis", "Centro", "Rua A, 100"),
        )
        oferta_expirada.status = StatusOferta.EXPIRADA
        oferta_expirada._estabelecimento_id = self.est.cnpj
        self.ctrl_of._metodos.inserir(self.ctrl_of._oferta_para_documento(oferta_expirada, self.est))
        self.ctrl_of._ofertas.append(oferta_expirada)

        consumidor = Consumidor(
            None, [], 0, agora, "maria@email.com", 1,
            Localizacao("Florianópolis", "Centro", "Av. Brasil, 50"), "Maria", "abc123",
        )
        reserva = Reserva(1, consumidor, oferta_ativa, agora + timedelta(hours=4))
        self.ctrl_res.adicionar_reserva(reserva)

        sucesso, msg = self.ctrl_est.editar_cadastro_estabelecimento(self.est, {
            "nome_fantasia": "Padaria Sol Nova",
            "tipo": "restaurante",
            "endereco": "Rua Nova, 999",
            "bairro": "Trindade",
            "cidade": "Florianópolis",
            "senha_atual": "",
            "nova_senha": "",
            "confirmar_senha": "",
        })
        self.assertTrue(sucesso, msg)

        atual = self.sistema.estabelecimento_logado
        self.assertEqual(atual.nome_fantasia, "Padaria Sol Nova")
        self.assertEqual(atual.tipo, TipoEstabelecimento.RESTAURANTE)
        self.assertEqual(atual.endereco, "Rua Nova, 999")
        self.assertEqual(atual.bairro, "Trindade")

        # RN04: oferta ativa recebe nova localização
        self.ctrl_of.recarregar_ofertas()
        of1 = self.ctrl_of.buscar_oferta(1, "Padaria Sol Nova")
        self.assertIsNotNone(of1)
        self.assertEqual(of1.localizacao.bairro, "Trindade")
        self.assertEqual(of1.localizacao.endereco, "Rua Nova, 999")

        # Oferta expirada mantém localização histórica, mas mantém vínculo
        of2 = self.ctrl_of.buscar_oferta(2, "Padaria Sol Nova")
        self.assertIsNotNone(of2)
        self.assertEqual(of2.localizacao.bairro, "Centro")

        # Reserva mantém vínculo com novo nome fantasia
        self.ctrl_res.recarregar_reservas()
        self.assertEqual(self.ctrl_res.todas_reservas()[0].oferta.nome_estabelecimento, "Padaria Sol Nova")

    def test_rn10_bloqueia_cnpj_e_email(self):
        ok_cnpj, _ = self.ctrl_est.editar_cadastro_estabelecimento(self.est, {
            "nome_fantasia": "Padaria Sol",
            "tipo": "padaria",
            "endereco": "Rua A, 100",
            "bairro": "Centro",
            "cidade": "Florianópolis",
            "cnpj": "99999999000100",
        })
        self.assertFalse(ok_cnpj)

        ok_email, _ = self.ctrl_est.editar_cadastro_estabelecimento(self.est, {
            "nome_fantasia": "Padaria Sol",
            "tipo": "padaria",
            "endereco": "Rua A, 100",
            "bairro": "Centro",
            "cidade": "Florianópolis",
            "email": "outro@padariasol.com",
        })
        self.assertFalse(ok_email)

        self.ctrl_est.atualizar_estabelecimento(self.est, {
            "cnpj": "00000000000100",
            "email": "hack@email.com",
            "nome_fantasia": "Padaria Sol Editada",
        })
        doc = self.ctrl_est._metodos.buscar_um({"cnpj": "12345678000199"})
        self.assertIsNotNone(doc)
        self.assertEqual(doc["email"], "contato@padariasol.com")
        self.assertEqual(doc["nome_fantasia"], "Padaria Sol Editada")

    def test_rf19_rn12_alterar_senha(self):
        base = {
            "nome_fantasia": "Padaria Sol",
            "tipo": "padaria",
            "endereco": "Rua A, 100",
            "bairro": "Centro",
            "cidade": "Florianópolis",
        }
        ok, _ = self.ctrl_est.editar_cadastro_estabelecimento(self.est, {
            **base, "senha_atual": "errada", "nova_senha": "nova456", "confirmar_senha": "nova456",
        })
        self.assertFalse(ok)

        ok, _ = self.ctrl_est.editar_cadastro_estabelecimento(self.est, {
            **base, "senha_atual": "", "nova_senha": "nova456", "confirmar_senha": "nova456",
        })
        self.assertFalse(ok)

        ok, _ = self.ctrl_est.editar_cadastro_estabelecimento(self.est, {
            **base, "senha_atual": "senha123", "nova_senha": "nova456", "confirmar_senha": "diferente",
        })
        self.assertFalse(ok)

        ok, _ = self.ctrl_est.editar_cadastro_estabelecimento(self.est, {
            **base, "senha_atual": "senha123", "nova_senha": "nova456", "confirmar_senha": "nova456",
        })
        self.assertTrue(ok)
        self.assertIsNone(self.ctrl_est.realizarLogin({"email": "contato@padariasol.com", "senha": "senha123"}))
        self.assertIsNotNone(self.ctrl_est.realizarLogin({"email": "contato@padariasol.com", "senha": "nova456"}))

    def test_navegacao_perfil_estabelecimento(self):
        tela_mock = self.ctrl_est._ControladorEstabelecimento__tela_estabelecimento
        tela_mock.perfil_estabelecimento.side_effect = [
            {
                "acao": "editar",
                "dados": {
                    "nome_fantasia": "Padaria Navegada",
                    "tipo": "mercado",
                    "endereco": "Rua Y, 2",
                    "bairro": "Kobrasol",
                    "cidade": "São José",
                    "senha_atual": "",
                    "nova_senha": "",
                    "confirmar_senha": "",
                },
            },
            "ofertas",
        ]
        self.ctrl_est._navegar_abas("perfil")
        self.assertEqual(self.sistema.estabelecimento_logado.nome_fantasia, "Padaria Navegada")
        self.assertEqual(self.sistema.estabelecimento_logado.tipo, TipoEstabelecimento.MERCADO)


if __name__ == "__main__":
    unittest.main()
