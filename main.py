from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/', methods=["GET", 'POST'])
def index_page():
    addr = str(request.remote_addr)
    result = {'place': 'None'}
    if request.method == 'POST':
        query = request.form.to_dict()['query']
        result = {'place': "1 стилаж, 2 ряд, 3 коробка", 'item': 'Зеленая горловина'}

    return render_template('index.html', result=result, addr=addr)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
