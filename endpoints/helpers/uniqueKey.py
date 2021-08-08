from time import time
import random


class hashable_object:
    def __init__(self, name):
        self.timestamp = int(time() * 1000)
        self.random_num = random.random()
        self.name = name

    def __hash__(self):
        return hash((self.timestamp, self.random_num, self.name))


def unique_key(user):
    hash_obj = hashable_object(user)
    print(f"hash obj type: {type(hash(hash_obj))}")
    return hash(hash_obj)
