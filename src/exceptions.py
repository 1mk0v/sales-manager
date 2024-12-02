
class BaseAPIException(BaseException):
    def __init__(self, *args: object, message:str, status_code:int) -> None:
        super().__init__(*args)
        self.message = message
        self.status_code = status_code