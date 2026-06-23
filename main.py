from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiItMSIsImV4cCI6NDkwNTU4MzU3MiwiaWF0IjoxNzUxOTgzNTcyLCJhdXRob3JpdGllcyI6W119.d7Eh_LOGqA44BH58HIiPrPIz1SLskVOPj4BRsae05cI"
HEADERS = {"authorization": f"Bearer {TOKEN}"}

@app.route('/quote/<isin>')
def get_quote(isin):
    mic = request.args.get("mic", "XMIL")
    url = f"https://grafici.borsaitaliana.it/api/instruments/{isin},{mic},ISIN/intraday?resolution=1MN"
    r = requests.get(url, headers=HEADERS, timeout=10)
    data = r.json()
    points = data.get("intradayPoint", [])
    if not points:
        return jsonify({"error": "no data"}), 404
    last = points[-1]
    date = last["time"].split("-")[0]
    close = last["endPx"]
    return jsonify([{
        "date": date,
        "close": close
    }])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
