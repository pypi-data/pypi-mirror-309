import json
from json import JSONEncoder


class Discount(object):
    def __init__(self, codigo, quantidadeDias, taxa, valor):
        self.code = codigo
        self.quantity_days = quantidadeDias
        self.rate = taxa
        self.value = valor

    def __eq__(self, other):
        if not isinstance(other, Discount):
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
        return json.dumps(self, cls=DiscountEncoder)

    @staticmethod
    def from_json(json_discount):
        data = json.loads(json_discount)
        return Discount(**data)


class DiscountEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
