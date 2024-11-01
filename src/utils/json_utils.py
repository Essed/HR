import aiofiles
import json
import os

async def add_data_to_json(data, filename):
    json_data = list()        
    json_data = await read_data_from_json_as_list(filename)
    json_data.append(data)
    await write_data_to_json_as_list(json_data, filename)


async def read_data_from_json_as_list(filename) -> list[dict]:
    data = list()
    if os.path.exists(filename):
        async with aiofiles.open(filename, 'r', encoding='utf-8') as file:
            content = await file.read()
            data = json.loads(content)
    return data


async def write_data_to_json_as_list(data, filename) -> list[dict]:
    async with aiofiles.open(filename, 'w', encoding='utf-8') as file:
        json_list: list = json.dumps(data, ensure_ascii=False, indent=4) 
        await file.write(json_list)
