from flask import Flask, render_template, request
import requests
import csv

app = Flask(__name__)

def export_items_to_csv():
 response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
 data = response.json()
 with open('rates.csv', 'w', newline='', encoding="utf-8") as csvfile:
    fieldnames = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in data:
     for rate in item['rates']:
       writer.writerow({'currency': rate['currency'], 'code': rate['code'], 'bid': rate['bid'],  'ask': rate['ask']})

items = []  
@app.route("/currency")
def currency():
 with open('rates.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
   items.append({'code':row['code'], 'ask':float(row['ask'])})
 return render_template("currency_calculator.html", items=items)

@app.route("/currency", methods=["post"])
def cost():
 code = request.form['code']
 amount = int(request.form['amount'])
 for item in items:
   if code==item['code']:
    cost = round(item['ask'] * amount, 2)
 return render_template("currency_calculator.html", code=code, amount=amount, items=items, cost=cost)

if __name__ =='__main__':
 app.run(debug=True)