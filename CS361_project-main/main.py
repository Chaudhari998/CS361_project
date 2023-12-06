from flask import Flask, render_template, request, redirect, url_for
import json
import os
from sender import convert_currency


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

    # Convert total spendings to EUR, CAD, and JPY
    converted_spendings = convert_currency('USD', ['EUR', 'CAD', 'JPY'], total_spendings)

    return render_template('index.html', spendings=spendings, 
                           total_spendings=total_spendings,
                           converted_spendings=converted_spendings)

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

@app.route('/edit/<int:index>', methods=['POST'])
def edit_spending(index):
    spendings = read_spendings()
    data = request.json

    # Update the specific transaction
    if 0 <= index < len(spendings):
        spendings[index] = {
            'description': data['description'],
            'amount': data['amount']
        }
        write_spendings(spendings)

    return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['DELETE'])
def delete_spending(index):
    spendings = read_spendings()

    # Delete the specific transaction
    if 0 <= index < len(spendings):
        del spendings[index]
        write_spendings(spendings)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
