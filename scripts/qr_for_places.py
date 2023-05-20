from PIL import Image, ImageDraw, ImageFont
import qrcode
import fitz


def generate_qr(link):
    img = qrcode.make(link)
    img.save("cache/qr.png")
    image = Image.open('cache/qr.png')
    flipped_image = image.rotate(180)
    flipped_image.save('cache/qr.png')


def create_image(text1, text2, text3):
    width = 800
    height = 400
    background_color = (255, 255, 255)
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)
    font_size = 80
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
    draw.text((text3_x, text3_y), text3, font=font, fill=font_color)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save("cache/title.png")


def create_pdf():
    img_rect1 = fitz.Rect(10, -1100, 910, -50)
    img_rect2 = fitz.Rect(10, -100, 860, 500)
    document = fitz.open('cache/template.pdf')
    page = document[0]
    page.insert_image(img_rect1, filename='cache/qr.png')
    page.insert_image(img_rect2, filename='cache/title.png')
    document.save('cache/result.pdf')
    document.close()


def execute(data):
    create_image(f"Стеллаж: {data['stellash']}", f'Полка: {data["polka"]}', f"Секция: {data['section']}")
    generate_qr(
        f"http://92.255.110.184:8000/connect-place?stellash={data['stellash']}&polka={data['polka']}&section={data['section']}")
    create_pdf()
