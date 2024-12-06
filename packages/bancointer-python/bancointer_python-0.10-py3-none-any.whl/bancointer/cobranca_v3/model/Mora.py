import json
from json import JSONEncoder
from numbers import Number


class Mora(object):
    def __init__(self, codigo: str, valor: Number, taxa: Number, *args, **kwargs):
        self.code = codigo
        self.value = valor
        self.rate = taxa

    def __eq__(self, other):
        if not isinstance(other, Mora):
            return NotImplemented
        return (
            self.code == other.code
            and self.rate == other.rate
            and self.value == other.value
        )

    def to_dict(self):
        return {
            "codigo": self.code,
            "valor": self.value,
            "taxa": self.rate,
        }

    def to_json(self):
        return json.dumps(self, cls=MoraEncoder)

    @staticmethod
    def from_json(json_discount):
        data = json.loads(json_discount)
        return Mora(**data)


class MoraEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
