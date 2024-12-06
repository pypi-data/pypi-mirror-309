import json
from numbers import Number

from bancointer.cobranca_v3.models.desconto import Desconto
from bancointer.cobranca_v3.models.message import Message
from bancointer.cobranca_v3.models.mora import Mora
from bancointer.cobranca_v3.models.multa import Multa
from bancointer.cobranca_v3.models.pessoa import Pessoa


class SolicitacaoEmitirCobranca(object):
    def __init__(
        self,
        seuNumero,
        valorNominal: Number,
        dataVencimento,
        numDiasAgenda: Number,
        pagador: Pessoa,
        desconto: Desconto,
        multa: Multa,
        mora: Mora,
        mensagem: Message,
        beneficiarioFinal: Pessoa | None = None,
        *args,
        **kwargs
    ):
        self.seu_numero = seuNumero
        self.valor_nominal = valorNominal
        self.data_vencimento = dataVencimento
        self.num_dias_agenda = numDiasAgenda
        self.pagador = pagador
        self.desconto = desconto
        self.multa = multa
        self.mora = mora
        self.mensagem = mensagem
        self.benificiario_final = beneficiarioFinal

    def to_dict(self):
        if self.benificiario_final is not None:
            return {
                "seuNumero": self.seu_numero,
                "valorNominal": self.valor_nominal,
                "dataVencimento": self.data_vencimento,
                "numDiasAgenda": self.num_dias_agenda,
                "pagador": self.pagador.to_dict(),
                "desconto": self.desconto.to_dict(),
                "multa": self.multa.to_dict(),
                "mora": self.mora.to_dict(),
                "mensagem": self.mensagem.to_dict(),
                "beneficiarioFinal": self.benificiario_final.to_dict(),
            }
        else:
            return {
                "seuNumero": self.seu_numero,
                "valorNominal": self.valor_nominal,
                "dataVencimento": self.data_vencimento,
                "numDiasAgenda": self.num_dias_agenda,
                "pagador": self.pagador.to_dict(),
                "desconto": self.desconto.to_dict(),
                "multa": self.multa.to_dict(),
                "mora": self.mora.to_dict(),
                "mensagem": self.mensagem.to_dict(),
            }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_request):
        data = json.loads(json_request)
        seu_numero = data["seuNumero"]
        valor_nominal = data["valorNominal"]
        data_vencimento = data["dataVencimento"]
        num_dias_agenda = data["numDiasAgenda"]
        pagador_data = data["pagador"]
        desconto_data = data["desconto"]
        multa_data = data["multa"]
        mora_data = data["mora"]
        mensagem_data = data["mensagem"]
        beneficiario_final_data = None
        if data["beneficiarioFinal"] is not None:
            beneficiario_final_data = data["beneficiarioFinal"]
        # Get dicts data
        pagador = Pessoa(**pagador_data)
        desconto = Desconto(**desconto_data)
        multa = Multa(**multa_data)
        mora = Mora(**mora_data)
        mensagem = Message(**mensagem_data)
        if beneficiario_final_data is not None:
            beneficiario_final = Pessoa(**beneficiario_final_data)
            return SolicitacaoEmitirCobranca(
                seu_numero,
                valor_nominal,
                data_vencimento,
                num_dias_agenda,
                pagador,
                desconto,
                multa,
                mora,
                mensagem,
                beneficiario_final,
            )
        else:
            return SolicitacaoEmitirCobranca(
                seu_numero,
                valor_nominal,
                data_vencimento,
                num_dias_agenda,
                pagador,
                desconto,
                multa,
                mora,
                mensagem,
            )
