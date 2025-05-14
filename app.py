from flask import Flask, request, jsonify
from config import Config

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Import models only after app is created to avoid circular imports
from models import db, Sale

# Initialize database with Flask app
db.init_app(app)

# Create tables on first request
@app.before_first_request
def create_tables():
    db.create_all()

# Route to add a new sale
@app.route("/sales", methods=["POST"])
def add_sale():
    data = request.get_json()
    new_sale = Sale(product=data["product"], amount=data["amount"])
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({"message": "Sale recorded"}), 201

# Route to retrieve all sales
@app.route("/sales", methods=["GET"])
def get_sales():
    sales = Sale.query.all()
    return jsonify([{"id": s.id, "product": s.product, "amount": s.amount} for s in sales])

# Run the app locally
if __name__ == "__main__":
    app.run()
