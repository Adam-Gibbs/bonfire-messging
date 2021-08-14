from time import time
import random
import boto3
import string

client_db = boto3.client('dynamodb')


class hashable_object:
    def __init__(self, name):
        self.timestamp = int(time() * 1000)
        self.random_num = random.random()
        self.name = name

    def __hash__(self):
        return hash((self.timestamp, self.random_num, self.name))


def unique_key(user, table, key_name):
    hash_obj = hashable_object(user)
    return check_unique(hash(hash_obj), table, key_name)


def randomword():
    return ''.join(random.choice(string.ascii_letters) for _ in range(10))


def check_unique(key, table, key_name):
    resp = client_db.get_item(
        TableName=table,
        Key={
            key_name: {'S': f"{key}"}
        }
    )

    if resp is None:
        return key
    else:
        return unique_key(randomword(), table, key_name)
