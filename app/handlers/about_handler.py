import json
from random import randint


def about_handler() -> str:
    with open("data/bvlarnaca.json", "r") as file:
        data = json.load(file)
    if not data:
        return "Mock!"
    return data[randint(0, len(data) - 1)]
