import database as db

class User():

    def __init__(self, id:int, name:str, surename:str, patronomic:str, role:str, office_id:str) -> None:
        self.id = id
        self.name = name
        self.surename = surename
        self.patronomic = patronomic
        self.roleName = role
        self.officeId = office_id

    def getInitials(self):
        return f"{self.surename} {self.name[0]}. {self.patronomic[0]}."
    
    async def getHashedAuthInfo(self):
        conn = await db.getConnection()
        conn.fetchrow("""SELECT * FROM user_auth as where id = $1""", self.id)


class UserAuth():
    def __init__(self, login:str, passwordHash:str, userId:int):
        self.login = login
        self.passwordHash = passwordHash
        self.userId = userId