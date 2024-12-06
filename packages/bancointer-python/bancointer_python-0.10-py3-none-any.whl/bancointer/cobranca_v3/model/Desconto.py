import json
from json import JSONEncoder


class Desconto(object):
    def __init__(self, code, quantity_days, rate, value):
        self.code = code
        self.quantity_days = quantity_days
        self.rate = rate
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Desconto):
            return NotImplemented
        return (
            self.code == other.code
            and self.quantity_days == other.quantity_days
            and self.rate == other.rate
            and self.value == other.value
        )

    def to_dict(self):
        return {
            "taxa": self.rate,
            "codigo": self.code,
            "quantidadeDias": self.quantity_days,
            "valor": self.value,
        }

    def to_json(self):
        return json.dumps(self, cls=DescontoEncoder)

    @staticmethod
    def from_json(json_discount):
        data = json.loads(json_discount)
        return Desconto(**data)


class DescontoEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
