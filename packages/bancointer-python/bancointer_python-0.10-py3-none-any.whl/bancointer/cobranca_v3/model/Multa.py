import json
from json import JSONEncoder


class Multa(object):
    def __init__(self, codigo, taxa, valor, *args, **kwargs):
        self.code = codigo
        self.rate = taxa
        self.value = valor

    def __eq__(self, other):
        if not isinstance(other, Multa):
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
        return json.dumps(self, cls=MultaEncoder)

    @staticmethod
    def from_json(json_discount):
        data = json.loads(json_discount)
        return Multa(**data)


class MultaEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
