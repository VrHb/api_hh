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


def get_vacancies_info(hh_api_params: dict) -> None:
    response = requests.get(HH_API_URL, params=hh_api_params)
    response.raise_for_status()
    return response.json()


def get_found_vacancies(hh_api_params: dict) -> None:
    response = requests.get(HH_API_URL, params=hh_api_params)
    response.raise_for_status()
    return response.json()["found"]


def get_vacancies_payment_range(hh_api_params: dict) -> list:
    response = requests.get(HH_API_URL, params=hh_api_params)
    response.raise_for_status()
    vacancies_salary = []
    for item in response.json()["items"]:
         vacancies_salary.append(item["salary"])
    return vacancies_salary


def predict_rub_salary(vacancy: dict) -> float | None:
    if vacancy["currency"] == "RUR":
        if vacancy["from"] and vacancy["to"]:
            payment = (vacancy["from"] + vacancy["to"]) / 2
            return payment
        elif vacancy["from"]:
            payment = vacancy["from"] * 1.2
            return payment
        elif vacancy["to"]:
            payment = vacancy["to"] * 0.8
            return payment
    else:
        return None


def main():
    python_vacancies = get_found_vacancies(
        {
        "specialization": 1.221,
        "area": 1,
        "period": 30,
        "text": "Программист Python"
        }
    )
    javascript_vacancies = get_found_vacancies(
        {
        "specialization": 1.221,
        "area": 1,
        "period": 30,
        "text": "Программист javascript"
        }
    )
    ruby_vacancies = get_found_vacancies(
        {
        "specialization": 1.221,
        "area": 1,
        "period": 30,
        "text": "Программист ruby"
        }
    )
    java_vacancies = get_found_vacancies(
        {
        "specialization": 1.221,
        "area": 1,
        "period": 30,
        "text": "Программист java"
        }
    )
    php_vacancies = get_found_vacancies(
        {
        "specialization": 1.221,
        "area": 1,
        "period": 30,
        "text": "Программист php"
        }
    )
    cplus_vacancies = get_found_vacancies(
        {
        "specialization": 1.221,
        "area": 1,
        "period": 30,
        "text": "Программист c++"
        }
    )
    c_vacancies = get_found_vacancies(
        {
        "specialization": 1.221,
        "area": 1,
        "period": 30,
        "text": "Программист c"
        }
    )
    csharp_vacancies = get_found_vacancies(
        {
        "specialization": 1.221,
        "area": 1,
        "period": 30,
        "text": "Программист c#"
        }
    )
    top_vacancies = {
        "python": python_vacancies,
        "Java": java_vacancies,
        "Javascript": javascript_vacancies,
        "PHP": php_vacancies,
        "C#": csharp_vacancies,
        "C++": cplus_vacancies,
        "RUBY": ruby_vacancies,
        "C": c_vacancies
    }
    
    python_vacancies_payments = get_vacancies_payment_range(
        {
            "text": "программист python",
            "salary": 180000,
            "curency": "RUR"
        }
    )
    
    print(top_vacancies)
    print("-----------------------------------------------------------------")
    print(python_vacancies_payments)
    print("-----------------------------------------------------------------")
    print(predict_rub_salary(python_vacancies_payments[9]))

if __name__ == "__main__":
    main()
