from core.data import UserData


class User:
    def __init__(self, user_data: UserData) -> None:
        self.__items = user_data.items

    def UserData(self, **update):
        return UserData.from_items(self.__items | update)
