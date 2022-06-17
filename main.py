import os
from dataclasses import dataclass
from enum import Enum

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable



@dataclass
class Vacancy:
    payment_from: int | None
    payment_to: int | None
    currency: str | None


class Programming_languages(str, Enum):
    JAVA = "java"
    PYTHON = "python"
    CPLUS = "c++"
    CSHARP = "c#"
    PHP = "php"
    JS = "java script"
    RUBY = "ruby"
    C = "c"


def get_vacancies_payment_range_from_hh(hh_api_params: dict) -> list:
    vacancies_salary = []
    page = 0
    page_number = 1
    while page < page_number:
        hh_api_params["page"] = page
        page_response = requests.get(
            "https://api.hh.ru/vacancies", 
            params=hh_api_params
        )
        page_response.raise_for_status()
        for item in page_response.json()["items"]:
            if item["salary"]:
                vacancies_salary.append(item["salary"])
        page_number = page_response.json()["pages"]
        page += 1
    return vacancies_salary


def predict_rub_salary(vacancy: Vacancy) -> float | None:
    if vacancy.currency == "RUR" or vacancy.currency == "rub":
        if vacancy.payment_from and vacancy.payment_to:
            payment = (vacancy.payment_from + vacancy.payment_to) / 2
            return payment
        elif vacancy.payment_from:
            payment = vacancy.payment_from * 1.2
            return payment
        elif vacancy.payment_to:
            payment = vacancy.payment_to * 0.8
            return payment
    return None


def get_average_salary_from_hh(vacancies_salary: list) -> int:
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
            url="https://api.superjob.ru/2.0/vacancies",
            headers=headers,
            params=params
        )
        page_response.raise_for_status()
        for item in page_response.json()["objects"]:
            sj_vacancies_total.append(item)
        page_number = int(page_response.json()["total"] % 20)
        page += 1
    return sj_vacancies_total
 

def get_average_salary_from_sj(vacancies_salary: list) -> int:
    salary = 0
    for vacancy_salary in vacancies_salary:
        if predict_rub_salary(vacancy_salary):
            salary += predict_rub_salary(vacancy_salary)
    return int(salary / len(vacancies_salary))
  

def create_table_output(
    table_name: str, 
    finded_vacancies: list,
    ordered_vacancies: list) -> str:
    table_data = [
        ["Язык програмирования", "Вакансий найдено", "Вакансий обработано"], 
    ]
    programming_languages = [language.value for language in Programming_languages]
    table_rows = list(zip(programming_languages, finded_vacancies, ordered_vacancies))
    for row in table_rows:
        table_data.append(list(row))
    table = AsciiTable(table_data, table_name)
    return table.table


def main():
    load_dotenv()

    """
    ##########################################################################
    HeadHunter block
    ##########################################################################
    """
    hh_sum_vacancies = []
    for language in Programming_languages:
        response = requests.get(
            url="https://api.hh.ru/vacancies",
            params={
                "specialization": 1.221,
                "area": 1,
                "text": f"Программист {language.value}"
            }
        )
        hh_sum_vacancies.append(response.json()["found"])


    hh_rub_vacancies = []
    for language in Programming_languages:
        vacancies_payment_range = get_vacancies_payment_range_from_hh({
            "specialization": 1.221,
            "area": 1,
            "text": f"Программист {language.value}"
        })
        hh_rub_vacancies_payments = []
        for vacancy_payment_range in vacancies_payment_range:
            vacancy = Vacancy(
            vacancy_payment_range["from"],
            vacancy_payment_range["to"],
            vacancy_payment_range["currency"]
            )
            if predict_rub_salary(vacancy):
                hh_rub_vacancies_payments.append(vacancy_payment_range)
        hh_rub_vacancies.append(len(hh_rub_vacancies_payments))
                    
    
    hh_table = create_table_output(
        "HeadHunter Moskow", 
        hh_sum_vacancies, 
        hh_rub_vacancies
        ) 
    

    """
    ##########################################################################
    SuperJob block
    ##########################################################################
    """
    sj_sum_vacancies = []
    for language in Programming_languages:
        response = requests.get(
            url="https://api.superjob.ru/2.0/vacancies",
            headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
            params={
                "keyword": f"Программист {language.value}",
                "town": 4
            }
        )
        sj_sum_vacancies.append(response.json()["total"])


    sj_rub_vacancies = []
    for language in Programming_languages:
        vacancies_payment_range = requests.get(
            url="https://api.superjob.ru/2.0/vacancies",
            headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
            params={
                "town": 4,
                "keyword": f"Программист {language.value}"
            }
        )
        sj_rub_vacancies_payments = []
        for vacancy_payment_range in vacancies_payment_range.json()["objects"]:
            vacancy = Vacancy(
            vacancy_payment_range["payment_from"],
            vacancy_payment_range["payment_to"],
            vacancy_payment_range["currency"]
            )
            if predict_rub_salary(vacancy):
                sj_rub_vacancies_payments.append(vacancy_payment_range)
        sj_rub_vacancies.append(len(sj_rub_vacancies_payments))


    sj_table = create_table_output(
        "SuperJob Moskow", 
        sj_sum_vacancies, 
        sj_rub_vacancies
        ) 


    print(hh_table)
    print(sj_table)

if __name__ == "__main__":
    main()

