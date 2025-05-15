from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales.db'  # Adjust if using PostgreSQL or other
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String(100), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Create DB tables (only for dev — not for production use)
with app.app_context():
    db.create_all()

@app.route("/sales", methods=["POST"])
def add_sale():
    data = request.get_json()

    try:
        product = data["product"]
        price = data["price"]
        quantity = data["quantity"]
        timestamp = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        amount = price * quantity

        new_sale = Transaction(
            product=product,
            price=price,
            quantity=quantity,
            amount=amount,
            timestamp=timestamp
        )
        db.session.add(new_sale)
        db.session.commit()
        return jsonify({"message": "Sale added successfully"}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing key: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sales", methods=["GET"])
def get_sales():
    date_str = request.args.get("date")  # expected format: YYYY-MM-DD
    if not date_str:
        return jsonify({"error": "Missing 'date' query param"}), 400

    start = f"{date_str} 00:00:00"
    end = f"{date_str} 23:59:59"

    sales = Transaction.query.filter(Transaction.timestamp.between(start, end)).all()
    result = [{
        "product": s.product,
        "price": s.price,
        "quantity": s.quantity,
        "amount": s.amount,
        "timestamp": s.timestamp
    } for s in sales]

    return jsonify(result)

@app.route("/frequency/<product_name>", methods=["GET"])
def price_frequency(product_name):
    sales = Transaction.query.filter_by(product=product_name).all()
    frequency = {}
    for s in sales:
        price = int(s.price)
        frequency[price] = frequency.get(price, 0) + 1
    return jsonify(frequency)

if __name__ == "__main__":
    app.run(debug=True)
