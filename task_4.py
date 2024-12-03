import json
import os
from collections import Counter
from bs4 import BeautifulSoup

def safe_float(value):
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def parsing_files(filename):
    
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    clothings = BeautifulSoup(content, 'xml')
    parsed_data = []

    for item in clothings.find_all('clothing'):

            clothings_data = {

                    'id': item.find('id').get_text()
                    .strip()
                    if item.find('id')
                    else None,
                    
                    'name': item.find('name').get_text()
                    .strip()
                    if item.find('name')
                    else None,

                    'category': item.find('category').get_text()
                    .strip()
                    if item.find('category')
                    else None,

                    'size': item.find('size').get_text()
                    .strip()
                    if item.find('size')
                    else None,
                    
                    'color': item.find('color').get_text()
                    .strip()
                    if item.find('color')
                    else None,

                    'material': item.find('material').get_text()
                    .strip()
                    if item.find('material')
                    else None,

                    'price': item.find('price').get_text()
                    .replace('billion years', '')
                    .strip()
                    if item.find('price')
                    else None,

                    'rating': item.find('rating').get_text()
                    .replace('million km', '')
                    .strip()
                    if item.find('rating')
                    else None,

                    'exclusive': item.find('exclusive').get_text()
                    .strip()
                    if item.find('exclusive')
                    else 'no',

                    'reviews': item.find('reviews').get_text()
                    .strip()
                    if item.find('reviews')
                    else None,

                    'sporty': item.find('sporty').get_text()
                    .strip()
                    if item.find('sporty')
                    else 'no',

                    'new': item.find('new').get_text()
                    .strip()
                    if item.find('new')
                    else '-'
        }
            parsed_data.append(clothings_data)

    return parsed_data

all_data = []  
    
input_folder = '/root/lab3/task_files/4'

for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)
    if os.path.isfile(filepath) and filename.endswith('.xml'):
        result = parsing_files(filepath)
        all_data.extend(result)

with open('/root/lab3/results/results4/all_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=1)

sorted_color = sorted(all_data, key=lambda x: x.get('color', '').lower())

with open('/root/lab3/results/results4/sorted_color.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_color, f, ensure_ascii=False, indent=1)

reviews = [int(clothings_data['reviews']) for clothings_data in all_data if 'reviews' in clothings_data and clothings_data['reviews'] is not None]

if reviews:

    min_reviews = min(reviews)
    max_reviews= max(reviews)
    avg_reviews = sum(reviews) / len(reviews)

else:

    min_reviews = max_reviews = avg_reviews = None

stat = {
    'reviews': {
        'Минимальное значение': min_reviews,
        'Максимальное значение': max_reviews,
        'Среднее значение': avg_reviews
    }
}

with open('/root/lab3/results/results4/stat_reviews.json', 'w', encoding='utf-8') as f:
    json.dump(stat, f, ensure_ascii=False, indent=1)

material = [clothings_data['material'] for clothings_data in all_data if 'material' in clothings_data]

material_freq = Counter(material)

with open('/root/lab3/results/results4/material_freq.json', 'w', encoding='utf-8') as f:
    json.dump(material_freq, f, ensure_ascii=False, indent=1)