import requests
from bs4 import BeautifulSoup
import re
import time

s = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
s.get("https://lk.sut.ru/cabinet/?login=yes", headers=headers)

def login_bonch(login, password):
    data = {'users': login,
            'parole': password}
    r = s.post("https://lk.sut.ru/cabinet/lib/autentificationok.php", data = data, headers=headers)
    return r.text


def sign(rasp, week):
    data = {'open': '1',
            'rasp': rasp,
            'week': week}

    r = s.post("https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie.php", data = data, headers=headers)
    return r.text

def get_sign(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        lesson = soup.find('a', text = "Начать занятие").get("onclick")
        numb = re.findall('(\d+)', str(lesson))
        sign(numb[0], numb[1])
        return True
    except Exception:
        print("Невозможно начать занятие.. Мы автоматически повторим попытку через 5 минут.")
        return False


try:
    f = open("logins.txt").readlines()
    login = f[0].replace("\n", "")
    password = f[1]

except Exception as e:
    print(e)
    input("Press Enter to close the program")
    exit(404)

logged = login_bonch(login, password)
if '1' == logged:
    print("Подключено через Email: %s.." % login)
    while(1):
        r = s.post("https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie.php", headers=headers)

        if r.text.__contains__("У Вас нет прав доступа. Или необходимо перезагрузить приложение.."):
            logged = login_bonch(login, password)

        if get_sign(r.text):
            break
        else:
            time.sleep(300)
else:
    print("Не получилось подключиться..\nВозможно вы ввели неверный логин или пароль.")


input("Press Enter to close the program")
