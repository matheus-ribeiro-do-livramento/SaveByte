from enum import Enum

class StatusOferta(Enum):
    DISPONIVEL = "disponivel"
    ESGOTADA = "esgotada"
    EXPIRADA = "expirada"
    CANCELADA = "cancelada"


class StatusReserva(Enum):
    PENDENTE = "pendente"
    RETIRADA = "retirada"
    EXPIRADA = "expirada"
    CANCELADA = "cancelada"


class TipoEstabelecimento(Enum):
    PADARIA = "padaria"
    RESTAURANTE = "restaurante"
    MERCADO = "mercado"


class TipoNotificacao(Enum):
    NOVA_OFERTA = "nova_oferta"
    LEMBRETE_RETIRADA = "lembrete_retirada"
    PENALIDADE = "penalidade"
    ESTORNO = "estorno"


class PreferenciaAlimentar(Enum):
    VEGETARIANO = "vegetariano"
    VEGANO = "vegano"
    SEM_GLUTEN = "sem_gluten"
    SEM_LACTOSE = "sem_lactose"

#Feito por Matheus