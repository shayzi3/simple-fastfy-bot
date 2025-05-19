from random import choice
from string import digits


async def generate_skin_id() -> int:
     return int("".join([choice(digits) for _ in range(9)]))