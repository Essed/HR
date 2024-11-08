from typing import Union
from src.enums import Role
from src.utils.json_utils import add_data_to_json, read_data_from_json_as_list, write_data_to_json_as_list, clear_data
from src.models.models import User

class UserAPI:
    def __init__(self, storage_path: str) -> None:
        self.__storage_path = storage_path

    async def register(self, user: User) -> User:
        users = await read_data_from_json_as_list(self.__storage_path)
        user_model = user.model_dump()
        if user_model not in users:
            await add_data_to_json(user_model, self.__storage_path)

        return user
    
    async def exist(self, user_id: int) -> bool:        
        users = await read_data_from_json_as_list(self.__storage_path)
        users = [User.model_validate(user).id for user in users]

        return True if user_id in users else False

    async def handle_user(self, username: str) -> Union[User, None]:
        users = await read_data_from_json_as_list(self.__storage_path)
        users = [User.model_validate(user) for user in users]
        users = [user for user in users if user.username == username]
        
        return users.pop() if len(users) != 0 else None

    async def update(self, user_id: int, updated_user: User):
        users = await read_data_from_json_as_list(self.__storage_path)
        users = [User.model_validate(user) for user in users]
        
        for index in range(0, len(users)):
            if users[index].id == user_id:
                users[index] = updated_user
        
        users = [user.model_dump() for user in users]
        await clear_data(self.__storage_path)
        await write_data_to_json_as_list(users, self.__storage_path)

    async def check_owner(self, user_id: int) -> bool:
        users = await read_data_from_json_as_list(self.__storage_path)
        users = [User.model_validate(user) for user in users]
        users = [user for user in users if user.role == Role.ADMIN and user.id == user_id]

        return True if len(users) > 0 else False