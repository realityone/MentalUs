class MentalUsException(Exception):
    code = 0

    def to_json(self):
        return dict(code=self.code, msg=self.msg)

