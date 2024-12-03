import json
import os
from collections import Counter
from bs4 import BeautifulSoup

def parsing_files(filename):

    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    item = {}
    soup = BeautifulSoup(content, 'html.parser')

    all_spans = soup.find_all('span')
    art_and_nal = soup.find('span')
    art_and_nal_text = art_and_nal.get_text()
    art = art_and_nal_text.split('Артикул:')[1].split('Наличие:')[0].strip()
    nal = art_and_nal_text.split('Наличие:')[1].strip()
    item['Артикул'] = art
    item['Наличие'] = nal

    name = soup.find('h1', class_='title')
    item['Название'] = name.get_text().replace('Название:', '').strip()

    city_and_price = soup.find('p', class_='address-price')
    city_and_price_text = city_and_price.get_text()
    city = city_and_price_text.split('Город:')[1].split('Цена:')[0].strip()
    price = city_and_price_text.split('Цена:')[1].replace('руб', '').strip()
    item['Город'] = city
    item['Цена'] = int(price)

    color = soup.find('span', class_='color')
    item['Цвет'] = color.get_text().replace('Цвет:', '').strip()

    quantity = soup.find('span', class_='quantity')
    item['Количество'] = int(quantity.get_text().replace('Количество:', '').replace('шт', '').strip())

    item['Размеры'] = all_spans[3].get_text().replace('Размеры:', '').strip()

    item['Ссылка на изображение'] = soup.find('img')['src']

    item['Рейтинг'] = float(all_spans[4].get_text().replace('Рейтинг:', '').strip())

    item['Просмотры'] = int(all_spans[5].get_text().replace('Просмотры:', '').strip())

    return item

input_folder = '/root/lab3/task_files/1'

all_items = []

for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)

    if os.path.isfile(filepath) and filename.endswith('.html'):
        result = parsing_files(filepath)
        all_items.append(result)

with open('/root/lab3/results/results1/all_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_items, f, ensure_ascii=False, indent=1)

sorted_items = sorted(all_items, key=lambda x: x.get('Цвет', '').lower())

with open('/root/lab3/results/results1/sorted_data.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_items, f, ensure_ascii=False, indent=1)

nal = [item['Наличие'] for item in all_items if 'Наличие' in item]

nal_freq = Counter(nal)

with open('/root/lab3/results/results1/nal_freq.json', 'w', encoding='utf-8') as f:
    json.dump(nal_freq, f, ensure_ascii=False, indent=1)

price_stat = [item['Цена'] for item in all_items if 'Цена' in item]

if price_stat:
    min_price = min(price_stat)
    max_price = max(price_stat)
    avg_price = round(sum(price_stat) / len(price_stat), 2)

else:
    min_price = max_price = avg_price = None

stat = {
    'Цена': {
        'Минимальное значение': min_price,
        'Максимальное значение': max_price,
        'Среднее значение': avg_price
    }
}

with open('/root/lab3/results/results1/stat_price.json', 'w', encoding='utf-8') as f:
    json.dump(stat, f, ensure_ascii=False, indent=1)