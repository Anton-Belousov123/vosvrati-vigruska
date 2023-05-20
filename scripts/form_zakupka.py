import json
from openpyxl import Workbook
import requests

headers = {
    'Client-Id': '667260',
    'Api-Key': '835f30d9-7159-4956-97f0-5f6353f93aab'
}


def get_codes():
    url = 'https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list'
    data = {
        "dir": "ASC",
        "filter": {
            "status": "awaiting_packaging",
            "cutoff_from": "2021-08-24T14:15:22Z",
            "cutoff_to": "2100-08-31T14:15:22Z"
        },
        "limit": 1000,
        "offset": 0,
        "with": {
            "analytics_data": True,
            "barcodes": True,
            "financial_data": True,
            "translit": True
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()['result']['postings']
    answer = []
    for i in response:
        answer.append([i['products'][0]['offer_id'], i['products'][0]['quantity']])
    return answer


def execute():
    codes = get_codes()
    workbook = Workbook()
    sheet = workbook.active
    for row in codes:
        sheet.append(row)
    workbook.save('cache/data.xlsx')