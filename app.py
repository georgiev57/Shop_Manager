from flask import Flask, request, jsonify
from config import Config
from models import db, Sale
from datetime import datetime, date

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Safely create tables on startup using app context
with app.app_context():
    db.create_all()

@app.route("/sales", methods=["POST"])
def add_sale():
    data = request.get_json()
    new_sale = Sale(
        product=data["product"],
        amount=data["amount"]
        # timestamp auto-set by default
    )
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({"message": "Sale recorded"}), 201

@app.route("/sales", methods=["GET"])
def get_sales():
    sales = Sale.query.all()
    return jsonify([
        {"id": s.id, "product": s.product, "amount": s.amount, "timestamp": s.timestamp.isoformat()}
        for s in sales
    ])

@app.route("/sales/today", methods=["GET"])
def get_sales_today():
    today = date.today()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())
    sales = Sale.query.filter(Sale.timestamp >= start, Sale.timestamp <= end).all()
    return jsonify([
        {"id": s.id, "product": s.product, "amount": s.amount, "timestamp": s.timestamp.isoformat()}
        for s in sales
    ])

if __name__ == "__main__":
    app.run()
