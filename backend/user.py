class User:
    username: str = ""
    password: bytes = ""
    first_name: str = ""
    last_name: str = ""

    ok = True

    def __init__(self, response: tuple[str, ]) -> None:
        if response is None:
            self.ok = False
            return
        self.first_name = response[0]
        self.last_name  = response[1]
        self.username   = response[2]
        self.password   = response[3].encode()

    def to_tuple(self) -> tuple[str]:
        return(self.first_name, self.last_name, self.username, self.password)
    
    def get_token(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    def __bool__(self):
        return self.ok