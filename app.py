from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector

app = Flask(__name__)

# -------- DATABASE CONNECTION --------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tharuni@2004",
        database="restaurant_db"
    )

# -------- HOME --------
@app.route('/')
def home():
    return render_template("index.html")

# -------- ADD TO CART --------
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    connection = get_connection()
    cursor = connection.cursor()

    data = request.get_json()
    item_name = data.get('item_name')
    price = data.get('price')

    cursor.execute("SELECT quantity FROM orders WHERE item_name=%s", (item_name,))
    result = cursor.fetchone()

    if result:
        new_quantity = result[0] + 1
        cursor.execute(
            "UPDATE orders SET quantity=%s WHERE item_name=%s",
            (new_quantity, item_name)
        )
    else:
        cursor.execute(
            "INSERT INTO orders (item_name, price, quantity) VALUES (%s, %s, %s)",
            (item_name, price, 1)
        )

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Item added successfully"})

# -------- VIEW CART --------
@app.route('/cart')
def cart():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM orders")
    items = cursor.fetchall()

    total = sum(item[2] * item[3] for item in items)

    cursor.close()
    connection.close()

    return render_template("cart.html", items=items, total=total)

# -------- DELETE SINGLE ITEM --------
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM orders WHERE id=%s", (item_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('cart'))

# -------- CLEAR CART --------
@app.route('/clear_cart')
def clear_cart():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM orders")
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)