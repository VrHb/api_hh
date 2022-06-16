import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable



@dataclass
class Vacancy:
    currency: str
    payment_to: float
    payment_from: float


def get_vacancies_payment_range_from_hh(hh_api_params: dict) -> list:
    vacancies_salary = []
    page = 0
    page_number = 1
    while page < page_number:
        hh_api_params["page"] = page
        page_response = requests.get("https://api.hh.ru/vacancies", params=hh_api_params)
        page_response.raise_for_status()
        for item in page_response.json()["items"]:
            vacancies_salary.append(item["salary"])
        page_number = page_response.json()["pages"]
        page += 1
    return vacancies_salary


def predict_rub_salary(vacancy: Vacancy) -> float | None:
    if vacancy.currency == "RUR":
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
        if predict_rub_salary_from_hh(vacancy_salary):
            salary += predict_rub_salary_from_hh(vacancy_salary)
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
    return None


def count_rub_vacancies_from_sj(vacancies: list) -> int:
    rub_vacancies = []
    for vacancy in vacancies:
        if vacancy["currency"] == "rub":
            rub_vacancies.append(vacancy)
    return len(rub_vacancies)


def main():
    load_dotenv()

    """
    ##########################################################################
    HeadHunter block
    ##########################################################################
    """

    python_vacancies = requests.get(
        url="https://api.hh.ru/vacancies",
        params={
            "specialization": 1.221,
            "area": 1,
            "text": "Программист Python"
        }
    )
    javascript_vacancies = get_vacancies_from_hh(
        {
            "specialization": 1.221,
            "area": 1,
            "text": "Программист javascript"
        }
    )
    ruby_vacancies = get_vacancies_from_hh(
        {
            "specialization": 1.221,
            "area": 1,
            "text": "Программист ruby"
        }
    )
    java_vacancies = get_vacancies_from_hh(
        {
            "specialization": 1.221,
            "area": 1,
            "text": "Программист java"
        }
    )
    php_vacancies = get_vacancies_from_hh(
        {
            "specialization": 1.221,
            "area": 1,
            "text": "Программист php"
        }
    )
    cplus_vacancies = get_vacancies_from_hh(
        {
            "specialization": 1.221,
            "area": 1,
            "text": "Программист c++"
        }
    )
    c_vacancies = get_vacancies_from_hh(
        {
            "specialization": 1.221,
            "area": 1,
            "text": "Программист c"
        }
    )
    csharp_vacancies = get_vacancies_from_hh(
        {
            "specialization": 1.221,
            "area": 1,
            "text": "Программист c#"
        }
    )

    python_vacancies_payments = get_vacancies_payment_range_from_hh(
        {
            "text": "программист python",
            "curency": "RUR",
            "only_with_salary": "true"
        }
    )
    
    java_vacancies_payments = get_vacancies_payment_range_from_hh(
        {
            "text": "программист java",
            "curency": "RUR",
            "only_with_salary": "true"
        }
    )
   
    c_vacancies_payments = get_vacancies_payment_range_from_hh(
        {
            "text": "программист java",
            "curency": "RUR",
            "only_with_salary": "true"
        }
    )

    cplus_vacancies_payments = get_vacancies_payment_range_from_hh(
        {
            "text": "программист c++",
            "curency": "RUR",
            "only_with_salary": "true"
        }
    )

    csharp_vacancies_payments = get_vacancies_payment_range_from_hh(
        {
            "text": "программист c#",
            "curency": "RUR",
            "only_with_salary": "true"
        }
    )
    
    php_vacancies_payments = get_vacancies_payment_range_from_hh(
        {
            "text": "программист php",
            "curency": "RUR",
            "only_with_salary": "true"
        }
    )
    ruby_vacancies_payments = get_vacancies_payment_range_from_hh(
        {
            "text": "программист ruby",
            "curency": "RUR",
            "only_with_salary": "true"
        }
    )
    js_vacancies_payments = get_vacancies_payment_range_from_hh(
        {
            "text": "программист java script",
            "curency": "RUR",
            "only_with_salary": "true"
        }
    )
    """
    ##########################################################################
    SuperJob block
    ##########################################################################
    """

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
    vacancies_sj_c = get_vacancies_from_sj(
        headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
        params={
            "keyword": "программист c",
        }
    )
    vacancies_sj_csharp = get_vacancies_from_sj(
        headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
        params={
            "keyword": "программист c#",
        }
    )
    vacancies_sj_cplus = get_vacancies_from_sj(
        headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
        params={
            "keyword": "программист c++",
        }
    )
    vacancies_sj_ruby = get_vacancies_from_sj(
        headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
        params={
            "keyword": "программист ruby",
        }
    )
    vacancies_sj_js = get_vacancies_from_sj(
        headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
        params={
            "keyword": "программист java script",
        }
    )
    vacancies_sj_php = get_vacancies_from_sj(
        headers={"X-Api-App-Id": os.getenv("SJ_API_KEY")},
        params={
            "keyword": "программист php",
        }
    )

    title_sj_table = "SuperJob Moskow"
    sj_table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано"],
        ["python", len(vacancies_sj_python), count_rub_vacancies_from_sj(vacancies_sj_python)],
        ["c", len(vacancies_sj_c), count_rub_vacancies_from_sj(vacancies_sj_c)],
        ["c#", len(vacancies_sj_csharp), count_rub_vacancies_from_sj(vacancies_sj_csharp)],
        ["c++", len(vacancies_sj_cplus), count_rub_vacancies_from_sj(vacancies_sj_cplus)],
        ["java", len(vacancies_sj_java), count_rub_vacancies_from_sj(vacancies_sj_java)],
        ["java script", len(vacancies_sj_js), count_rub_vacancies_from_sj(vacancies_sj_js)],
        ["ruby", len(vacancies_sj_ruby), count_rub_vacancies_from_sj(vacancies_sj_ruby)],
        ["php", len(vacancies_sj_php), count_rub_vacancies_from_sj(vacancies_sj_php)],
    ]
    sj_table = AsciiTable(sj_table_data, title_sj_table)
    print(sj_table.table)

    title_hh_table = "HeadHunter Moskow"
    hh_table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано"],
        ["python", python_vacancies, len(python_vacancies_payments)],
        ["c", c_vacancies, len(c_vacancies_payments)],
        ["c#", csharp_vacancies, len(csharp_vacancies_payments)],
        ["c++", cplus_vacancies, len(cplus_vacancies_payments)],
        ["java", java_vacancies, len(java_vacancies_payments)],
        ["java script", javascript_vacancies, len(js_vacancies_payments)],
        ["ruby", ruby_vacancies, len(ruby_vacancies_payments)],
        ["php", php_vacancies, len(php_vacancies_payments)],
    ]
    hh_table = AsciiTable(hh_table_data, title_hh_table)
    print(hh_table.table)


if __name__ == "__main__":
    main()

