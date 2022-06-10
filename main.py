import os 
import json
from typing import Final

from dotenv import load_dotenv
import requests


HH_API_URL: Final = "https://api.hh.ru/vacancies"
SJ_API_URL: Final = "https://api.superjob.ru/2.0/vacancies"

def get_access_token(oauth_data: dict):
    response = requests.post(
        url="https://hh.ru/oauth/token",
        data=oauth_data
    )
    return response.json()


def get_hh_vacancies_info(hh_api_params: dict) -> None:
    response = requests.get(HH_API_URL, params=hh_api_params)
    response.raise_for_status()
    return response.json()


def get_hh_found_vacancies(hh_api_params: dict) -> None:
    response = requests.get(HH_API_URL, params=hh_api_params)
    response.raise_for_status()
    return response.json()["found"]


def get_hh_vacancies_payment_range(hh_api_params: dict) -> list:
    vacancies_salary = []
    page = 0
    page_number = 1
    while page < page_number:
        hh_api_params["page"] = page
        page_response = requests.get(HH_API_URL, params=hh_api_params)
        page_response.raise_for_status()
        for item in page_response.json()["items"]:
            vacancies_salary.append(item["salary"])
        page_number = page_response.json()["pages"]
        page += 1
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


def get_average_hh_salary(vacancies_salary: list) -> int:
    salary = 0
    for vacancy_salary in vacancies_salary:
        if predict_rub_salary(vacancy_salary):
            salary += predict_rub_salary(vacancy_salary)
    return int(salary / len(vacancies_salary))


def get_vacancies_from_sj(params: dict, headers: dict) -> list:
    sj_vacancies_total = []
    page = 0
    page_number = 1
    while page < page_number:
        params["page"] = page
        page_response = requests.get(
            url=SJ_API_URL,
            headers=headers,
            params=params

        )
        page_response.raise_for_status()
        for item in page_response.json()["objects"]:
            sj_vacancies_total.append(item)
        page_number = int(page_response.json()["total"] / 20)
        page += 1
    return sj_vacancies_total
 

def get_average_sj_salary(vacancies_salary: list) -> int:
    salary = 0
    for vacancy_salary in vacancies_salary:
        if predict_rub_salary_for_sj(vacancy_salary):
            salary += predict_rub_salary_for_sj(vacancy_salary)
    return int(salary / len(vacancies_salary))

  

def predict_rub_salary_for_sj(vacancy: dict) -> float | None:
    if vacancy["currency"] == "rub":
        if vacancy["payment_from"] and vacancy["payment_to"]:
            payment = (vacancy["payment_from"] + vacancy["payment_to"]) / 2
            return payment
        elif vacancy["payment_from"]:
            payment = vacancy["payment_from"] * 1.2
            return payment
        elif vacancy["payment_to"]:
            payment = vacancy["payment_to"] * 0.8
            return payment
    else:
        return None


def main():
    load_dotenv()

    """
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
            "salary": 150000,
            "curency": "RUR",
            "only_with_salary": "true"
        }
    )
    
    java_vacancies_payments = get_vacancies_payment_range(
        {
            "text": "программист java",
            "salary": 150000,
            "curency": "RUR",
            "only_with_salary": "true"
        }
    )
    
    vacancies_hh_for_petia = {
        "python": {
            "vacancies_found": python_vacancies,
            "vacancies_processed": len(python_vacancies_payments),
            "average_salary": get_average_salary(python_vacancies_payments)
        },
        "java": {
            "cacancies_found": java_vacancies,
            "vacancies_processed": len(java_vacancies_payments),
            "average_salary": get_average_salary(java_vacancies_payments)
        }
    }

    print(top_vacancies)
    print("-----------------------------------------------------------------")
    print(python_vacancies_payments)
    print("-----------------------------------------------------------------")
    print(predict_rub_salary(python_vacancies_payments[9]))
    print("-----------------------------------------------------------------")
    print(vacancies_for_petia)
"""

    vacancies_sj_moskow = get_vacancies_from_sj(
        headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
        params={
            "town": "Москва",
            "keyword": "программист"
        }
    )
    for item in vacancies_sj_moskow:
        print("-------------------------------------------------------------")
        print(f'{item["profession"]}, {item["town"]["title"]}, {predict_rub_salary_for_sj(item)}')


    vacancies_sj_python = get_vacancies_from_sj(
        headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
        params={
            "keyword": "программист python",
        }
    )   
    vacancies_sj_java = get_vacancies_from_sj(
        headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
        params={
            "keyword": "программист java",
        }
    )   
    

    print("-------------------------------------------------------------")
    vacancies_sj_for_petia = {
        "Python": {
            "vacancies_found": len(vacancies_sj_python),
            "vacancies_processed": len(vacancies_sj_python),
            "average_salary": get_average_sj_salary(vacancies_sj_python)
        },
        "Java": {
            "vacancies_found": len(vacancies_sj_java),
            "vacancies_processed": len(vacancies_sj_java),
            "average_salary": get_average_sj_salary(vacancies_sj_java)
        }
    }
    print(vacancies_sj_for_petia)
    print("-------------------------------------------------------------")

"""
Нужно:
1. Убрать, объединить лишние функции
2. Разобраться с обработанными вакансиями, это выходит те, что оплачиваются в
рублях
3. Сделать вывод красивый
"""

if __name__ == "__main__":
    main()

