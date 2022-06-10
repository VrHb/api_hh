import json
from typing import Final

import requests


HH_API_URL: Final = "https://api.hh.ru/vacancies"


def get_access_token(oauth_data: dict):
    response = requests.post(
        url="https://hh.ru/oauth/token",
        data=oauth_data
    )
    return response.json()


def get_vacancy(hh_api_params: dict) -> None:
    response = requests.get(HH_API_URL, params=hh_api_params)
    response.raise_for_status()
    print(response.json())


def main():
    get_vacancy({"specialization": 1.221})



if __name__ == "__main__":
    main()
