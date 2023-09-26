import datetime

import requests


def get_people(people_id):
    return requests.get(f"https://swapi.dev/api/people/{people_id}").json()


def main():
    person_1 = get_people(1)
    person_2 = get_people(2)
    person_3 = get_people(3)
    person_4 = get_people(4)
    print(person_1, person_2, person_3, person_4)


if __name__ == "__main__":
    start = datetime.datetime.now()
    main()
    print(datetime.datetime.now() - start)
