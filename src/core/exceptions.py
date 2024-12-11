from exceptions import BaseAPIException

class NoAccessRights(BaseAPIException):
    def __init__(self, *args, message = "There are no rights to receive this information!", status_code = 400):
        super().__init__(*args, message=message, status_code=status_code)