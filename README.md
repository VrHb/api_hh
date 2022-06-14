# Сравниваем вакансии программистов
Данный проект помомает автоматизировать подбор вакансий на сайтах HeadHunter и SuperJob
## Как установить
* Необходимо установить интерпретатор python версии 3.10
* Cкопировать содержимое проекта к себе в рабочую директорию
* Активировать внутри рабочей директории виртуальное окружение:
```
python -m venv [название окружения]
```
* Установить зависимости(необходимые библиотеки):
```
pip install -r pip_requirements.txt
```
### Настройка переменных окружения:
* Для хранения переменных окружения создаем файл .env:
```
touch .env
```
* Регистрируем приложение и получаем ключ приложения для использования API SuperJob
по этой [ссыслке](https://api.superjob.ru/register), записываем его в .env файл:
```
echo "SJ_API_KEY='ваш ключ'" >> .env 
```
### Как пользоваться:
Запускаем файл:
```
python main.py
```
