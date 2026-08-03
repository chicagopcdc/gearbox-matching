

class PublishStudyMessageDetail:
    def __init__(self, code: str, value: str = None):
        self.code = code 
        self.value = value 

    def to_dict(self):
        return vars(self)

class PublishStudyMessage:
    def __init__(self, message: str, details: list[PublishStudyMessageDetail] = None):
        self.message = message
        self.details = details

    def to_dict(self):
        return {
            "message": self.message,
            "details": [x.to_dict() for x in self.details] if self.details else None
        }


def is_number(s: str):
    try:
        float(s)
        return True
    except ValueError:
        return False