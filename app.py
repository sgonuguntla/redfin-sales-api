from flask import Flask, request, jsonify
from redfin_scraper import get_redfin_sales

app = Flask(__name__)

@app.route("/estimate", methods=["POST"])
def estimate():
    data = request.json
    zip_code = data.get("zip")
    if not zip_code:
        return jsonify({"error": "Missing ZIP code"}), 400

    avg_price, comps = get_redfin_sales(zip_code)
    if avg_price:
        return jsonify({
            "estimated_price": avg_price,
            "comps": comps
        })
    else:
        return jsonify({"message": "Not enough sales data found"}), 404

if __name__ == "__main__":
    app.run()
