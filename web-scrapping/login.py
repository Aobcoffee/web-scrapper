import requests
from bs4 import BeautifulSoup


def login(payload: dict):

    login_url = 'https://shop.pier7.de/Shop/login.php?action=process'
    secure_url = 'https://shop.pier7.de/Shop/wish_list.php'

    with requests.session() as s:
        s.post(login_url, data=payload)
        r = s.get(secure_url)
        soup = BeautifulSoup(r.content, "html.parser")

        return soup


if __name__ == "__main__":
    ...