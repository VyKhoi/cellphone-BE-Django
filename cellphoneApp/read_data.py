import json
import os
from cellphoneApp.models import Smartphone

with open(os.path.join(os.getcwd(), 'data/json data/Smartphone.json')) as f:
    data = json.load(f)

for smartphone_data in data:
    smartphone = Smartphone.objects.create(
        id = smartphone_data['id'],
        name=smartphone_data['name'],
        nameManufacture=smartphone_data['nameManufacture'],
        operatorSystem=smartphone_data['operatorSystem'],
        CPU=smartphone_data['CPU'],
        RAM=smartphone_data['RAM'],
        ROM=smartphone_data['ROM'],
        Battery=smartphone_data['Battery'],
        Others=smartphone_data['Others']
    )