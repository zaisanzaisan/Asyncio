import asyncio
from datetime import datetime

import aiohttp as aiohttp

from db import begin_s, end_s, Session, Character


async def get_data(url: str):
    http_session = aiohttp.ClientSession()
    response = await http_session.get(url)
    json_data = await response.json()
    await http_session.close()
    return json_data


async def add_character(cid: int, data: dict):
    session = Session()
    c = Character(id=cid,
                  name=data["name"],
                  birth_year=data["birth_year"],
                  eye_color=data["eye_color"],
                  films=str(data["films"]),
                  gender=data["gender"],
                  hair_color=data["hair_color"],
                  height=data["height"],
                  home_world=data["homeworld"],
                  mass=data["mass"],
                  skin_color=data["skin_color"],
                  species=str(data["species"]),
                  starships=str(data["starships"]),
                  vehicles=str(data["vehicles"])
                  )
    session.add(c)
    await session.commit()


async def main():
    await begin_s()
    ppl_count = (await get_data(f'https://swapi.dev/api/people/')).get("count", 0)
    print(f"Got {ppl_count} characters")

    task_list = []
    for c in range(1, ppl_count):
        task_list.append(asyncio.Task(get_data(f'https://swapi.dev/api/people/{c}')))
    print(f"Created {len(task_list)} tasks for characters")

    for cnt, task in enumerate(task_list):
        resp = (await asyncio.gather(task))[0]
        if not (resp.get("detail") and resp.get("detail") == "Not found"):
            asyncio.Task(add_character(cnt + 1, resp))
            print(f"pushing character {cnt + 1} ({resp['name']}) to db")

    current_task = asyncio.current_task()
    tasks_sets = asyncio.all_tasks()
    tasks_sets.remove(current_task)
    await asyncio.gather(*tasks_sets)
    print(f"All job done .")

    await end_s()


if __name__ == "__main__":
    start = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start)
