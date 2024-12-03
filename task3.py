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

    stars = BeautifulSoup(content, 'xml')
    parsed_data = []

    for star in stars.find_all('star'):

            star_data = {
                    'name': star.find('name').get_text()
                    .strip(),

                    'constellation': star.find('constellation').get_text()
                    .strip()
                    if star.find('constellation')
                    else None,

                    'spectral-class': star.find('spectral-class').get_text()
                    .strip()
                    if star.find('spectral-class')
                    else None,
                    
                    'radius': safe_float(star.find('radius').get_text()
                    .strip())
                    if star.find('radius')
                    else None,

                    'rotation': safe_float(star.find('rotation').get_text()
                    .replace('days', '')
                    .strip())
                    if star.find('rotation')
                    else None,

                    'age': safe_float(star.find('age').get_text()
                    .replace('billion years', '')
                    .strip())
                    if star.find('age')
                    else None,

                    'distance': safe_float(star.find('distance').get_text()
                    .replace('million km', '')
                    .strip())
                    if star.find('distance')
                    else None,

                    'absolute-magnitude': safe_float(star.find('absolute-magnitude').get_text()
                    .replace('million km', '')
                    .strip())
                    if star.find('absolute-magnitude')
                    else None
        }
            parsed_data.append(star_data)

    return parsed_data

all_data = []  
    
input_folder = '/root/lab3/task_files/3'

for filename in os.listdir(input_folder):
    filepath = os.path.join(input_folder, filename)
    if os.path.isfile(filepath) and filename.endswith('.xml'):
        result = parsing_files(filepath)
        all_data.extend(result)

with open('/root/lab3/results/results3/all_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=1)

sorted_name = sorted(all_data, key=lambda x: x.get('name', '').lower())

with open('/root/lab3/results/results3/sorted_name.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_name, f, ensure_ascii=False, indent=1)

age = [float(star_data['age']) for star_data in all_data if 'age' in star_data and star_data['age'] is not None]

if age:
    min_age = min(age)
    max_age = max(age)
    avg_age = sum(age) / len(age)
else:
    min_age = max_age = avg_age = None

stat = {
    'age': {
        'Минимальное значение': min_age,
        'Максимальное значение': max_age,
        'Среднее значение': avg_age
    }
}

with open('/root/lab3/results/results3/stat_age.json', 'w', encoding='utf-8') as f:
    json.dump(stat, f, ensure_ascii=False, indent=1)

sp_class = [star_data['spectral-class'] for star_data in all_data if 'spectral-class' in star_data]
class_freq = Counter(sp_class)

with open('/root/lab3/results/results3/class_freq.json', 'w', encoding='utf-8') as f:
    json.dump(class_freq, f, ensure_ascii=False, indent=1)