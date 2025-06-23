import requests
from bs4 import BeautifulSoup
import csv

domain = 'https://atlas.herzen.spb.ru'
source_url = 'https://atlas.herzen.spb.ru/prof.php'

def get_persons(url):
    response = requests.get(url)
    my_soup = BeautifulSoup(response.text, 'html.parser')
    cells = my_soup.find_all('td', class_='t1')
    results = []

    for cell in cells:
        if cell.a:
            name = cell.a.text.strip()
            url = cell.a['href']
            item = {
                'name': name,
                'url': f"{domain}/{url}"
            }
            results.append(item)

    return results

def get_details(person):
    url = person['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    def extract_info(label):
        tag = soup.find('h3', class_='mm', string=label)
        if tag:
            p = tag.find_next_sibling('p', class_='mm1')
            if p and p.span:
                return p.span.text.strip()
        return ''

    person['degree_and_title'] = extract_info('Ученая степень и звание:')
    person['phone'] = extract_info('Контактный телефон:')
    person['email'] = extract_info('E-mail:')
    return person

# Собираем список преподавателей
data = []
for i in range(23):
    url = f'https://atlas.herzen.spb.ru/prof.php?FND=0&FIO=&PAGE={i}'
    data.extend(get_persons(url))

# Добавляем подробности
detailed_data = []
for person in data:
    try:
        detailed = get_details(person)
        detailed_data.append(detailed)
    except Exception as e:
        print(f"Ошибка при обработке {person['url']}: {e}")

# Сохраняем в CSV
with open('herzen_professors.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'url', 'degree_and_title', 'phone', 'email']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in detailed_data:
        writer.writerow(row)

print("Данные сохранены в herzen_professors.csv")
