from src.utils.json_utils import add_data_to_json, read_data_from_json_as_list
from src.models.models import User

class UserAPI:
    def __init__(self, storage_path: str):
        self.__storage_path = storage_path

    async def register(self, user: User) -> User:
        users = await read_data_from_json_as_list(self.__storage_path)
        user_model = user.model_dump()
        if user_model not in users:
            await add_data_to_json(user_model, self.__storage_path)

        return user
    
    async def exist(self, user_id: int):        
        users = await read_data_from_json_as_list(self.__storage_path)
        pass