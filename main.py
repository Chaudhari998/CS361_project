from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File paths
SPENDINGS_FILE = 'spendings.json'

# Read spendings from the file
def read_spendings():
    if not os.path.exists(SPENDINGS_FILE):
        return []

    with open(SPENDINGS_FILE, 'r') as file:
        spendings = json.load(file)
        return spendings

# Write spendings to the file
def write_spendings(spendings):
    with open(SPENDINGS_FILE, 'w') as file:
        json.dump(spendings, file, indent=4)

@app.route('/')
def index():
    spendings = read_spendings()
    total_spendings = sum(float(spd['amount']) for spd in spendings)
    return render_template('index.html', spendings=spendings, total_spendings=total_spendings)

@app.route('/add', methods=['POST'])
def add_spending():
    description = request.form.get('description')
    amount = request.form.get('amount')
    
    # Read current spendings, add the new one, then write back to the file
    spendings = read_spendings()
    spendings.append({
        'description': description,
        'amount': amount
    })
    write_spendings(spendings)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
