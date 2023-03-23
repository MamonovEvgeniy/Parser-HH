import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json


def get_links(text):
    """Функция для получения ссылок на вакансий по заданному поисковому запросу.
       Функция считает количество страниц и берёт ссылки на вакансии на каждой из этих страниц в цикле.
       В функцию передаётся текст запроса."""
    # Объект useragent для создания заголовка.
    ua = fake_useragent.UserAgent()
    result = requests.get(
        url=f"https://hh.ru/search/vacancy?text={text}&from=suggest_post&area=113&customDomain=1",
        headers={"user-agent": ua.random}
    )
    if result.status_code != 200:
        return
    # Контент страницы в переменной soup.
    soup = BeautifulSoup(result.content, "lxml")
    # Количество страниц по заданному поисковому запросу.
    try:
        page_count = int(soup.find("div", attrs={"class": "pager"})
                         .find_all("span", recursive=False)[-1].find("a").find("span").text)
    except Exception:
        return

    for page in range(page_count):
        try:
            result = requests.get(
                url=f"https://hh.ru/search/vacancy?text={text}&from=suggest_post&area=113&customDomain=1&page={page}",
                headers={"user-agent": ua.random}
            )
            if result.status_code != 200:
                continue
            soup = BeautifulSoup(result.content, "lxml")
            for a in soup.find_all("a", attrs={"class": "serp-item__title"}):
                yield f"{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"{e}")
        # добавляем задержку в 1 секунду после каждого запроса
        time.sleep(1)


def get_vacancies(link):
    """Функция для получения данных о вакансии: название вакансии, название компании, требуемый опыт, зарплата, теги и ссылка.
     В функцию передаётся ссылка и создаётся объект вакансии"""
    ua = fake_useragent.UserAgent()
    result = requests.get(
        url=link,
        headers={"user-agent": ua.random}
    )
    if result.status_code != 200:
        return
    soup = BeautifulSoup(result.content, "lxml")
    # Название вакансии
    try:
        name = soup.find(attrs={"class": "vacancy-title"}).find("h1").text
    except Exception:
        name = ""
    # Название компании
    try:
        company = soup.find(attrs={"class": "vacancy-company-name"}).find("a").find("span").text.replace(" ", " ")
    except Exception:
        company = ""
    # Требуемый опыт
    try:
        experience = soup.find(attrs={"class": "vacancy-description-list-item"}).find("span").text
    except Exception:
        experience = ""
    # Зарплата
    try:
        salary = soup.find(attrs={"class": "vacancy-title"}).find("span").text.replace("\xa0", " ")
    except Exception:
        salary = "Зарплата не указана"
    # Тэги
    try:
        tags = [tag.text.replace(" ", " ") for tag in soup.find(attrs={"class": "bloko-tag-list"}).find_all("span", attrs={"class": "bloko-tag__section_text"})]
    except Exception:
        tags = []
    # Объект вакансии
    vacancy = {
        "title": name,
        "company": company,
        "experience": experience,
        "salary": salary,
        "tags": tags,
        "link": link,
    }
    return vacancy


if __name__ == "__main__":
    data = []
    for a in get_links("python"):
        data.append(get_vacancies(a))
        time.sleep(1)
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
