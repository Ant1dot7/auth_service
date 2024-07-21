import random
import string


def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def make_post_data():
    with open('post_data.txt', 'w') as f:
        for i in range(1000_000):  # создаем 1000 уникальных запросов
            username = random_string(10)
            email = f"{username}@mail.com"
            data = f'{{"username": "{username}", "password": "string", "email": "{email}", "date_birth": "2024-07-07"}}'
            f.write(f"http://127.0.0.1:8000/users/ POST {data}\n")


def make_get_urls():
    with open('urls.txt', 'w') as f:
        for i in range(1, 1000_000 + 1):  # создаем 1000 уникальных запросов
            f.write(f"http://127.0.0.1:8000/users/{i}\n")

make_get_urls()