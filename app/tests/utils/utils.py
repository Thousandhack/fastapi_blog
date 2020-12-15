from app.core.config import settings
import random
import string


def get_server_api():
    return f'http://{settings.SERVER_NAME}:{settings.SERVER_PORT}{settings.API_V1_STR}'


def generate_access_token_headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}


def random_lower_string(length):
    return "".join(random.choices(string.ascii_lowercase, k=length))


def generate_random_username():
    return random_lower_string(32)


def generate_random_email():
    return f'{random_lower_string(32)}@{random_lower_string(32)}.com'


def generate_random_password():
    return random_lower_string(16)

