# app.py
from flask import Flask, render_template, request, redirect, url_for
from shop_logic import Order

app = Flask(__name__)
current_order = Order()

@app.route('/')
def index():
    total = current_order.calculate_total()
    return render_template('index.html', order=current_order, total=total)

@app.route('/add', methods=['POST'])
def add_item():
    price = float(request.form.get('price', 0))
    current_order.add_item(price)
    return redirect(url_for('index'))

@app.route('/checkout', methods=['POST'])
def checkout():
    if current_order.state == "cart":
        current_order.transition_state("placed")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
