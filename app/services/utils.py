import time
from uuid import uuid4

def generate_unique_token():
    return str(int(time.time())) + str(uuid4())