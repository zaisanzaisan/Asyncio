import asyncio
import datetime

import aiohttp
from more_itertools import chunked

from models import Base, Session, SwapiPeople, engine

MAX_CHUNK_SIZE = 10


async def get_people(people_id):
    session = aiohttp.ClientSession()
    response = await session.get(f"https://swapi.dev/api/people/{people_id}")
    json_data = await response.json()
    await session.close()
    return json_data


async def insert_to_db(people_json_list):
    async with Session() as session:
        swapi_people_list = [
            SwapiPeople(json=json_data) for json_data in people_json_list
        ]
        session.add_all(swapi_people_list)
        await session.commit()


async def main():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    for ids_chunk in chunked(range(1, 91), MAX_CHUNK_SIZE):
        get_people_coros = [get_people(people_id) for people_id in ids_chunk]
        people_json_list = await asyncio.gather(*get_people_coros)
        asyncio.create_task(insert_to_db(people_json_list))

    current_task = asyncio.current_task()
    tasks_sets = asyncio.all_tasks()
    tasks_sets.remove(current_task)

    await asyncio.gather(*tasks_sets)
    await engine.dispose()


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)
