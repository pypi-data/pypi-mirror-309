import json
from json import JSONEncoder

from bancointer.cobranca_v3.models.desconto import Desconto
from bancointer.cobranca_v3.models.message import Message
from bancointer.cobranca_v3.models.mora import Mora
from bancointer.cobranca_v3.models.multa import Multa
from bancointer.cobranca_v3.models.pessoa import Pessoa


class RequisicaoEmitirCobranca(object):
    def __init__(
        self,
        seu_numero,
        valor_nominal,
        data_vencimento,
        num_dias_agenda,
        pagador: Pessoa,
        desconto: Desconto,
        multa: Multa,
        mora: Mora,
        mensagem: Message,
        benificiario_final: Pessoa,
        *args,
        **kwargs
    ):
        self.seu_numero = seu_numero
        self.valor_nominal = valor_nominal
        self.data_vencimento = data_vencimento
        self.num_dias_agenda = num_dias_agenda
        self.pagador = pagador
        self.desconto = desconto
        self.multa = multa
        self.mora = mora
        self.mensagem = mensagem
        self.benificiario_final = benificiario_final

    def to_json(self):
        return json.dumps(self, cls=RequisicaoEmitirCobrancaEncoder)

    @staticmethod
    def from_json(json_request):
        data = json.loads(json_request)
        return RequisicaoEmitirCobranca(**data)


class RequisicaoEmitirCobrancaEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
