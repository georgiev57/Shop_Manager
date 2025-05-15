from flask import Flask, request, jsonify
from config import Config
from models import db, Transaction

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/sales", methods=["POST"])
def add_sale():
    data = request.get_json()
    new_sale = Transaction(product=data["product"], amount=data["amount"])
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({"message": "Sale recorded"}), 201

@app.route("/sales", methods=["GET"])
def get_sales():
    sales = Transaction.query.all()
    return jsonify([
        {
            "id": s.id,
            "product": s.product,
            "amount": s.amount,
            "timestamp": s.timestamp.isoformat()
        }
        for s in sales
    ])
