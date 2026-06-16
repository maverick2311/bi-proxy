from flask import Flask, jsonify
import requests

app = Flask(__name__)

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiItMSIsImV4cCI6NDkwNTU4MzU3MiwiaWF0IjoxNzUxOTgzNTcyLCJhdXRob3JpdGllcyI6W119.d7Eh_LOGqA44BH58HIiPrPIz1SLskVOPj4BRsae05cI"
HEADERS = {"authorization": f"Bearer {TOKEN}"}

@app.route('/quote/<isin>')
def get_quote(isin):
    url = f"https://grafici.borsaitaliana.it/api/instruments/{isin},XMIL,ISIN/intraday?resolution=1MN"
    r = requests.get(url, headers=HEADERS, timeout=10)
    data = r.json()
    points = data.get("intradayPoint", [])
    if not points:
        return jsonify({"error": "no data"}), 404
    p = points[0]
    return jsonify([{
        "date": p["previousClosingDt"],
        "close": p["previousClosingPx"]
    }])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
