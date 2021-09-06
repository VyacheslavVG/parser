import requests
import sqlite3
import re

from bs4 import BeautifulSoup as bs

def start_the_parser():
    conn = sqlite3.connect('../bd.db')# ПОДКЛЮЧЕНИЕ К БД
    cur = conn.cursor()
    conn.commit()
    cur.execute('DROP TABLE IF EXISTS freelance_ru;',) # ДЛЯ УДАЛЕНИЯ ТАБЛИЦЫ БД
    conn.commit()

    conn = sqlite3.connect('../bd.db')# ПОДКЛЮЧЕНИЕ К БД
    cur = conn.cursor()
    conn.commit()

    cur.execute(""" CREATE TABLE IF NOT EXISTS freelance_ru(
         id INTEGER  PRIMARY  KEY AUTOINCREMENT NOT NULL,
         title TEXT,
         date DATETIME,
         cost TEXT ,
         link TEXT)
    """) # КОД ДЛЯ СОЗДАНИЯ ТАБЛИЦЫ БАЗЫ ДАННЫХ
    conn.commit()


    for i in range(1,5,1) :
        # ЭТОТ КОД НЕОБХОДИМ ДЛЯ СКАЧКИ HTML ДОКУМЕНТА СТРАНИИЦЫ , ЧТОБЫ НЕ ДОЛБИТЬ САЙТ
        url = 'https://freelance.ru/project/search/pro?c=&q=python%2Cпарсер%2Cбот&m=or&e=&f=&t=&o=1https%3A%2F%2Fwww.fl.ru%2Fprojects&page='+str(i)+'&per-page=25'
        r =requests.get(url)
        src = r.text

        # ЭТОТ КОД НЕОБХОДИМ ДЛЯ СКАЧКИ HTML ДОКУМЕНТА СТРАНИИЦЫ , ЧТОБЫ НЕ ДОЛБИТЬ САЙТ
        with open('../index.html', 'w') as file: # СОЗДАНИЕ ФАЙЛА index.html , И ОТКРЫВАЕМ В РЕЖИМЕ ЗАПИСИ ПРИ КАЖДОМ ЗАПУСКЕ ПРОИСХОДИТ ПЕРЕЗАПИССЬ
           file.write(src) #ЗАПИСЫВАЕМ ПОЛУЧЕННЫЙ ФАЙЛВ index.html

        with open('../index.html') as file:
            src = file.read() #ОТКРЫВАЕМ ФАЙЛ ДЛЯ ЧТЕНИЯ И РАБОТЫ С НИМ
        soup = bs(src, 'lxml')

        all_jobs = soup.find_all(class_='title')# ПОИСК
        date = soup.find_all(class_='timeago')# ПО
        cost = soup.find_all(class_='cost')
        links = soup.find_all('a' , class_='description',)# КЛАССАМ
        link = []
        for i in links : # ЦИКЛ ДЛЯ ВЫТАСКИВАНИЯ ССЫЛОК С ТЕГОВ А
            url = i.get('href','-')
            link.append(url)
        a = []
        b = []
        c = 0
        d = []
        itog = []
        for el,elb,eld,ele in zip(all_jobs,date, cost ,link):
            item = el.text
            a.append(item.split()) #разбиваем строки по пробелам
            itemb = elb.text #ТЕМ САМЫМ УБИРАЕМ ЛИШНИЕ ПРОБЕЛЫ
            b.append(itemb.split()) # ДЛЯ КАЖДОГО СПАРСЕННОГО КЛАССА
            itemd = eld.text  # ДЕЛАЕМ СПИСКИ ПО КАЖДОМУ ИЗ КЛАССОВ В РЕЗУЛЬТАТЕ СПИСОК СПИСКОВ СЛОВ ДЛЯ КАЖДОГО ОБЪЯВЛЕНИЯ
            d.append(itemd.split()) # ДЕЛАЕМ СПИСКИ ПО КАЖДОМУ ИЗ КЛАССОВ В РЕЗУЛЬТАТЕ СПИСОК СПИСКОВ СЛОВ ДЛЯ КАЖДОГО ОБЪЯВЛЕНИЯ
        for el,elb,eld,ele in zip(a,b,d,link) :#
            el = ' '.join(el)# ОБЪЕДИНЯЕМ СПИСКИ СЛОВ
            eld = ' '.join(eld)# В ПРЕДЛОЖЕНИЯ ЧЕРЕЗ ПРОБЕЛЫ
            elb = ' '.join(elb)
            result = re.search('бот' , el)# ИЩЕМ В EL(ЗАГОЛОВКЕ) СЛОВО бот
            if result !=None :
                c+=1
                job = (el , elb , eld , 'https://freelance.ru' + ele)# ОБЪЕДИНЯЕМ ДАННЫЕ В КОРТЕЖ ДЛЯ ПЕРЕДАЧИ В БД
                itog.append(job)
                print(c , '--- ' + el + ' --- ' + elb + ' --- ' + eld + '---' + 'https://freelance.ru' + ele)
            result = re.search('парс' , el) # ИЩЕМ В EL(ЗАГОЛОВКЕ) СЛОВО ПАРС
            if result != None:
                c += 1
                job = (el, elb , eld , 'https://freelance.ru' + ele)# ОБЪЕДИНЯЕМ ДАННЫЕ В КОРТЕЖ ДЛЯ ПЕРЕДАЧИ В БД
                itog.append(job)
                print(c , '--- ' + el + ' --- ' + elb + ' --- ' + eld + ' --- '+ 'https://freelance.ru' + ele)


        conn = sqlite3.connect('../bd.db')
        cur = conn.cursor()

        conn.commit()
        for el in itog :
           cur.execute("INSERT INTO freelance_ru(title, date, cost,link) VALUES(?, ?, ?,?)", el) # доБАВЛЯЕМ ДАННЫЕ В ТАЬЛИЦУ бд
           conn.commit()

start_the_parser()

# conn = sqlite3.connect('bd.db')# ПОДКЛЮЧЕНИЕ К БД
# cur = conn.cursor()
# conn.commit()
#
# cur.execute(""" CREATE TABLE IF NOT EXISTS freelance_ru(
#      id INTEGER  PRIMARY  KEY AUTOINCREMENT NOT NULL,
#      title TEXT,
#      date DATETIME,
#      cost TEXT ,
#      content TEXT)
# """) # КОД ДЛЯ СОЗДАНИЯ БАЗЫ ДАННЫХ
# conn.commit()



