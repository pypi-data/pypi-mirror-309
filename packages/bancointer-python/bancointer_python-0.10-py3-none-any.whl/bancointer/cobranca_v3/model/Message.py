import json
from json import JSONEncoder


class Message(object):
    def __init__(self, linha1, linha2, linha3, linha4, linha5, *args, **kwargs):
        self.line_1 = linha1
        self.line_2 = linha2
        self.line_3 = linha3
        self.line_4 = linha4
        self.line_5 = linha5

    def __eq__(self, other):
        if not isinstance(other, Message):
            return NotImplemented
        return (
            self.line_1 == other.line_1
            and self.line_2 == other.line_2
            and self.line_3 == other.line_3
            and self.line_4 == other.line_4
            and self.line_5 == other.line_5
        )

    def to_dict(self):
        return {
            "linha1": self.line_1,
            "linha2": self.line_2,
            "linha3": self.line_3,
            "linha4": self.line_4,
            "linha5": self.line_5,
        }

    def to_json(self):
        return json.dumps(self, cls=MessageEncoder)

    @staticmethod
    def from_json(json_discount):
        data = json.loads(json_discount)
        return Message(**data)


class MessageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
