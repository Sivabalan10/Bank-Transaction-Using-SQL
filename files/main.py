from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_key_if_not_set')

def create_database():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS account_details
                 (username TEXT PRIMARY KEY, password TEXT, pancard TEXT, nominee TEXT, balance REAL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pancard = request.form['pancard']
        nominee = request.form['nominee']
        balance = 1000.0

        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute('INSERT INTO account_details (username, password, pancard, nominee, balance) VALUES (?, ?, ?, ?, ?)',
                  (username, password, pancard, nominee, balance))
        conn.commit()
        conn.close()
        flash('Account created successfully!')
        return redirect(url_for('index'))
    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        c.execute('SELECT * FROM account_details WHERE username=? AND password=?', (username, password))
        account = c.fetchone()
        conn.close()
        if account:
            return redirect(url_for('account', username=username))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/account/<username>', methods=['GET', 'POST'])
def account(username):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('SELECT * FROM account_details WHERE username=?', (username,))
    account = c.fetchone()
    conn.close()
    if not account:
        flash('Account not found')
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'withdraw' in request.form:
            amount = float(request.form['amount'])
            if amount <= account[4]:
                new_balance = account[4] - amount
                conn = sqlite3.connect('bank.db')
                c = conn.cursor()
                c.execute('UPDATE account_details SET balance=? WHERE username=?', (new_balance, username))
                conn.commit()
                conn.close()
                flash('Withdrawal successful!')
            else:
                flash('Insufficient balance')

        elif 'deposit' in request.form:
            amount = float(request.form['amount'])
            new_balance = account[4] + amount
            conn = sqlite3.connect('bank.db')
            c = conn.cursor()
            c.execute('UPDATE account_details SET balance=? WHERE username=?', (new_balance, username))
            conn.commit()
            conn.close()
            flash('Deposit successful!')

        elif 'change_pin' in request.form:
            new_password = request.form['new_password']
            conn = sqlite3.connect('bank.db')
            c = conn.cursor()
            c.execute('UPDATE account_details SET password=? WHERE username=?', (new_password, username))
            conn.commit()
            conn.close()
            flash('PIN changed successfully!')

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('SELECT * FROM account_details WHERE username=?', (username,))
    account = c.fetchone()
    conn.close()

    return render_template('account.html', account=account)

@app.route('/view_account_details/<username>')
def view_account_details(username):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('SELECT * FROM account_details WHERE username=?', (username,))
    account = c.fetchone()
    conn.close()
    if not account:
        flash('Account not found')
        return redirect(url_for('index'))
    return render_template('view_account_details.html', account=account)

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
