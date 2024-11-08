from src.utils.json_utils import add_data_to_json, read_data_from_json_as_list, clear_data, write_data_to_json_as_list
from src.models.models import Guild
from typing import List, Union

class GuildAPI:
    def __init__(self, storage_path: str):
        self.__storage_path = storage_path

    async def create(self, guild: Guild) -> Guild:
        guilds = await read_data_from_json_as_list(self.__storage_path)
        guild_model = guild.model_dump()
        if guild_model not in guilds:
            await add_data_to_json(guild_model, self.__storage_path)

        return guild
    
    async def exist(self, company_name: str) -> bool:        
        guilds = await read_data_from_json_as_list(self.__storage_path)
        if len(guilds) == 0:
            return False

        guilds = [Guild.model_validate(guild) for guild in guilds]
        guild = [Guild.model_validate(guild) for guild in guilds if guild.company_name == company_name]
        
        return True if len(guild) != 0 else False
    
    async def add_member(self, member: Union[str, List[str]], company_name: str) -> Union[Guild, None]:
        guilds = await read_data_from_json_as_list(self.__storage_path)
        guilds = [Guild.model_validate(guild) for guild in guilds]
        
        if len(guilds) == 0: 
            return None
        
        guild: Guild = [guild for guild in guilds if guild.company_name == company_name][0]
        guild.members.append(member)
        other_guilds = [guild for guild in guilds if guild.company_name != company_name]

        guilds = [guild for guild in other_guilds]
        guilds.append(guild)

        guild_models = [Guild.model_validate(guild).model_dump() for guild in guilds]
        
        await clear_data(self.__storage_path)
        await write_data_to_json_as_list(guild_models, self.__storage_path)        

        return guild