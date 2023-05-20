import json
from datetime import datetime, timedelta

import PyPDF2 as PyPDF2
import fitz
import qrcode
import requests
from PIL import Image, ImageDraw, ImageFont

headers = {
    'Client-Id': '667260',
    'Api-Key': '835f30d9-7159-4956-97f0-5f6353f93aab'
}


def download_image(url):
    response = requests.get(url, stream=True)
    with open('cache/item.png', 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
        file.close()

    from PIL import Image
    image = Image.open('cache/item.png')
    flipped_image = image.rotate(180)
    flipped_image.save('cache/item.png')


def get_data_from_api():
    now = datetime.now() - timedelta(days=4)  # TODO: in future delete timedelta
    time_from = now.replace(hour=0, minute=0, second=0, microsecond=0)
    time_to = now.replace(hour=23, minute=59, second=59, microsecond=0)
    time_from_str = time_from.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_to_str = time_to.strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {
        'filter': {
            'status': 'returned_to_seller',
            'accepted_from_customer_moment': {
                'time_from': time_from_str,
                'time_to': time_to_str
            }
        },
        'limit': 1000
    }
    response = requests.post('https://api-seller.ozon.ru/v3/returns/company/fbs', headers=headers,
                             data=json.dumps(data))
    result = []
    for i in response.json()['returns']:
        result.append({'article': i['product_id'], 'name': i['product_name'], 'quantity': i['quantity'], 'image': ''})
    return result


def get_image(product_id):
    url = 'https://api-seller.ozon.ru/v2/product/info'
    data = {
        "offer_id": '',
        "product_id": 0,
        "sku": product_id
    }
    resp = requests.post(url, data=json.dumps(data), headers=headers).json()
    return resp['result']['offer_id'], resp['result']['primary_image']


def generate_qr(link):
    img = qrcode.make(link)
    img.save("cache/qr.png")
    image = Image.open('cache/qr.png')
    flipped_image = image.rotate(180)
    flipped_image.save('cache/qr.png')


def generate_description(text1, text2, text3):
    if len(text2) > 40:
        text2 = text2[:40] + '...'
    width = 800
    height = 400
    background_color = (255, 255, 255)
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    font_size = 36
    font_color = (0, 0, 0)
    font_path = "cache/font.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text1_width, text1_height = draw.textsize(text1, font=font)
    text1_x = (width - text1_width) // 2
    text1_y = (height - (text1_height * 2)) // 2
    text2_width, text2_height = draw.textsize(text2, font=font)
    text2_x = (width - text2_width) // 2
    text2_y = text1_y + text1_height
    text3_width, text3_height = draw.textsize(text3, font=font)
    text3_x = (width - text3_width) // 2
    text3_y = text2_y + text2_height

    draw.text((text1_x, text1_y), text1, font=font, fill=font_color)
    draw.text((text2_x, text2_y), text2, font=font, fill=font_color)
    draw.text((text3_x, text3_y), '', font=font, fill=font_color)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save("cache/title.png")


def create_pdf(number):
    img_rect1 = fitz.Rect(40, -1100, 840, -400)
    img_rect3 = fitz.Rect(190, -400, 690, -100)
    img_rect2 = fitz.Rect(10, -100, 860, 500)
    document = fitz.open('cache/template.pdf')
    page = document[0]
    page.insert_image(img_rect1, filename='cache/qr.png')
    page.insert_image(img_rect2, filename='cache/title.png')
    page.insert_image(img_rect3, filename='cache/item.png')
    document.save(f'cache/result-{number}.pdf')
    document.close()


def concatenate_pdfs(number):
    pdf_writer = PyPDF2.PdfWriter()

    for idx in range(1, number + 1):
        with open(f'cache/result-{idx}.pdf', 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
    with open('cache/result.pdf', 'wb') as output:
        pdf_writer.write(output)
    output.close()


def execute():
    data = get_data_from_api()
    pages_count = 0
    for i in range(len(data)):
        article, image = get_image(data[i]['article'])
        data[i]['article'] = article
        data[i]['image'] = image
        for _ in range(data[i]['quantity']):
            pages_count += 1
            generate_qr(
                f'http://92.255.110.184:8000/connect-item?name={data[i]["name"]}&article={data[i]["article"]}&image={data[i]["image"]}')
            generate_description(text1=str(data[i]["article"]), text2=data[i]["name"], text3='')
            download_image(data[i]['image'])
            create_pdf(pages_count)
    concatenate_pdfs(pages_count)
