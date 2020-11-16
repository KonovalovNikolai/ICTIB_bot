import eventlet
import requests
import base64
from bs4 import BeautifulSoup

URL_GOG_API = "https://www.googleapis.com/customsearch/v1/siterestrict?key=AIzaSyDVqmE1G8CdDMnqJHj5dMZGyQlEV3X3eXo&" \
              "cx=62963ebbd0c56def7&q={}"


# получение данных
def get_data(url):
    """
    Получение данных из формированного запроса API. Функция принимает url запроса.
    Функция универсальная, работает с VK и Google Custom Search.
    """
    timeout = eventlet.Timeout(10)
    try:
        feed = requests.get(url)
        return feed.json()
    except eventlet.timeout.Timeout:
        return None
    finally:
        timeout.cancel()


def parsing(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    # Парсинг ФИО
    about_employee = soup.find('section', {'class': 'about_employee'})
    name = about_employee.find('h2').text.strip()

    # Поиск класса "text" и поиск в нём всех тегов <p>
    text = about_employee.find('div', 'text')
    tags_p = text.find_all('p')

    # Парсинг кафедры и звания
    department = []
    list_dep = []
    for item in tags_p:
        try:
            if item.a['href'][0] == '/':
                department.append(" ".join(item.text.replace('\n', '').split()))
        except TypeError:
            pass
    department = ", ".join(department)

    # Парсинг номеров телефонов
    phone = text.find('span', 'phones').text
    if len(phone) != 0:
        phone = phone.replace(';', '')
        phone = phone.replace('\n', '')
        phone = phone.replace(' ', '')
        phone = phone.replace('+', '\n+').strip()
        phone = phone.replace('д', ' д')

    # Парсинг почт
    contacts = text.find("div", "contacts")
    mails = []
    if contacts.script is not None:
        for item in contacts.script.next_siblings:
            item = str(item).replace("\n", "")
            if (first_comma := item.find("'")) != -1:
                second_comma = item.find("'", first_comma + 1)
                item = item[first_comma + 1:second_comma]
                item = str(base64.b64decode(item))
                index = item.find('"', 19)
                mails.append(item[26:index])

    # Формирование ответа
    mails = "\n".join(mails)
    answer = '{}\n{}\nТелефон: {}\nE-mail: {}\n<a href="{}">Источник</a>'.format(name, department, phone, mails, url)
    while answer.find("\n\n") != -1:
        answer = answer.replace("\n\n", "\n")
    return answer


def get_lecturer(intext=""):
    intext = intext.replace("+", "\+")  # при вводе номере
    intext = intext.replace("@", "\@")  # при вводе почты
    res = []
    data = get_data(URL_GOG_API.format("(inurl:p_per_id) " + intext))
    if not data:
        return 'Преподаватель не найден.'
    try:
        intext = data['spelling']['correctedQuery'][17:]
        data = get_data(URL_GOG_API.format(data['spelling']['correctedQuery'])
    except KeyError:
        pass
    try:
        url = data['items'][0]['link']
    except KeyError:
        return 'Преподаватель не найден.'
    res.append(url)

    for item in data['items'][1:]:
        if intext in item['title']:
            res.append(item['link'])
        if len(res) == 4:
            break

    return res


