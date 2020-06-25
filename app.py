import requests, datetime
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.
## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin') #얘랑 아래 겟메소드의 어드민 URL은 달라야함.
def admin():
    return render_template('admin_html.html')
## API 역할을 하는 부분

@app.route('/order', methods=['POST'])
def write_order():
    time = datetime.datetime.now()
    name_receive = request.form['name_give']
    price_receive = request.form['price_give']
    qty_receive = request.form['qty_give']
    # pay_receive = request.form['pay_give']
    order = {
        'time' : time,
        'name': name_receive,
        'price': price_receive,
        'qty': qty_receive,
        # 'pay': pay_receive
    }
    print(order)
    db.snack.insert_one(order)
    return jsonify({'result':'success', 'msg': '이 요청은 POST!'})


@app.route('/api/admin', methods=['GET'])
def read_orders():
    data = list(db.snack.find({}, {'_id': False}))
    print(data)
    return jsonify({'result':'success', 'msg': '이 요청은 GET!', 'orders': data})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)