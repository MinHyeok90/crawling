import requests
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('http://api.encar.com/search/car/list/premium?count=true&q=(And.Hidden.N._.(C.CarType.Y._.Manufacturer.%ED%98%84%EB%8C%80.)_.OfficeCityState.%EA%B2%BD%EA%B8%B0._.Trust.ExtendWarranty._.Options.%EB%B8%8C%EB%A0%88%EC%9D%B4%ED%81%AC+%EC%9E%A0%EA%B9%80+%EB%B0%A9%EC%A7%80(ABS_)._.Options.%ED%9B%84%EB%B0%A9+%EC%B9%B4%EB%A9%94%EB%9D%BC._.Options.%EC%A3%BC%EC%B0%A8%EA%B0%90%EC%A7%80%EC%84%BC%EC%84%9C(%EC%A0%84%EB%B0%A9_)._.Category.SUV.)&sr=%7CModifiedDate%7C0%7C100')
print(req.status_code)
print(req.headers.get("Content-Type"))
json_data = req.text

print("----")

with open(os.path.join(BASE_DIR, 'result.json'), 'w+',  encoding='UTF-8-sig') as json_file:
    json_file.write(json.dumps(json_data, ensure_ascii=False))
