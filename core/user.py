from core.data import UserData


class User:
    def __init__(self, user_data: UserData) -> None:
        self.__items = user_data.items
        self.__last_login = user_data.last_login
        self.__login_days = user_data.login_days

    def UserData(self, **update):
        return UserData.from_items(self.__items | update)

    @property
    def last_login(self):
        return self.__last_login

    @property
    def login_days(self):
        return self.__login_days
