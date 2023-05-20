from flask import Flask, render_template, request, send_file, redirect
from db import database
app = Flask(__name__)
user_stats = {}
mode = 0


@app.route('/connect-item', methods=['GET'])
def item_page():
    """http://127.0.0.1:5000/connect-item?name=test&article=123&image=https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5Qv-LaoGtRxcJ7rzQj9EMDgX0FiIDX3vuaEyAN73q&s&quantity=2"""
    global user_stats
    addr = str(request.remote_addr)
    name = request.args.get('name')
    article = request.args.get('article')
    image = request.args.get('image')
    item = {'name': name, 'article': article, 'image': image}
    user_stats[addr] = item
    return render_template('item-qr.html', item=item, is_new=True)


@app.route('/connect-place-accept', methods=["POST"])
def connect_page_page():
    database.connect_item(request.form.get('name'), request.form.get('article'), request.form.get('image'),
                          request.form.get('stellash'), request.form.get('polka'), request.form.get('section'))
    return render_template('success.html')


@app.route('/connect-place', methods=['GET'])
def place_page():
    addr = str(request.remote_addr)
    stellash = request.args.get('stellash')
    polka = request.args.get('polka')
    section = request.args.get('section')
    place = {'stellash': stellash, 'polka': polka, 'section': section}
    try:
        item = user_stats[addr]
    except:
        item = {}  # TODO: maybe bug
    if mode == 0:
        database.connect_item(item['name'], item['article'], item['image'], stellash, polka, section)
        return render_template('success.html')
    return render_template('place-qr.html', place=place, item=item, mode=mode)


@app.route('/', methods=["GET", 'POST'])
def index_page():
    addr = str(request.remote_addr)
    result = {'place': 'None'}
    if request.method == 'POST':
        query = request.form.to_dict()['query']
        item = database.select_item(query)
        if item:
            result = {'place': f"Стеллаж {item[3]}, полка {item[4]}, секция {item[5]}",
                      'item': f'[{item[1]}] {item[0]}', 'photo': item[2]}
    return render_template('index.html', result=result, addr=addr, mode=mode)


@app.route('/change-mode', methods=['POST'])
def change_mode_page():
    global mode
    if mode == 0:
        mode = 1
    else:
        mode = 0
    return redirect('/')


@app.route('/delete-item', methods=['POST'])
def delete_item_page():
    database.delete_item(request.form.get('article'))
    return render_template('success.html')


@app.route('/create-sticker-for-place', methods=['GET', "POST"])
def sticker_create_page():
    if request.method == 'POST':
        from scripts import qr_for_places
        qr_for_places.execute({'stellash': request.form.get('stellash'), 'polka': request.form.get('polka'),
                               'section': request.form.get('section')})
        return send_file('cache/result.pdf')

    data = {'stellash': 1, 'polka': 2, 'section': 3}
    return render_template('create-sticker.html')


@app.route('/download-stickers-for-item', methods=['POST'])
def download_stickers_for_item():
    from scripts import qr_for_items
    qr_for_items.execute()
    return send_file('cache/result.pdf')


@app.route('/download-today-order', methods=['GET'])
def download_today_order_page():
    from scripts import form_zakupka
    form_zakupka.execute()
    return send_file('cache/data.xlsx')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
