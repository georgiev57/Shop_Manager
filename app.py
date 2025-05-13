from flask import Flask, request, jsonify
from models import db, Sale
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/sales", methods=["POST"])
def add_sale():
    data = request.get_json()
    new_sale = Sale(product=data["product"], amount=data["amount"])
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({"message": "Sale recorded"}), 201

@app.route("/sales", methods=["GET"])
def get_sales():
    sales = Sale.query.all()
    return jsonify([{"id": s.id, "product": s.product, "amount": s.amount} for s in sales])

if __name__ == "__main__":
    app.run()
