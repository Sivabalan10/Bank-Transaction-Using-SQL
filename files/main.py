import sqlite3
import getpass

def create_database():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            pan_card TEXT NOT NULL,
            nominee_name TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 1000
        )
    ''')
    conn.commit()
    conn.close()

def create_account():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    pan_card = input("Enter PAN card number: ")
    nominee_name = input("Enter nominee name: ")
    balance = float(input("Enter initial balance: "))

    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO account_details (username, password, pan_card, nominee_name, balance)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password, pan_card, nominee_name, balance))
        conn.commit()
        print("Account created successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different username.")
    conn.close()

def check_credentials(username):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM account_details WHERE username = ?
    ''', (username,))
    account = cursor.fetchone()
    conn.close()
    return account

def withdraw_money(account):
    amount = float(input("Enter amount to withdraw: "))
    password = getpass.getpass("Enter password: ")

    if password != account[2]:
        print("Incorrect password.")
        return

    if amount <= 0:
        print("Invalid amount. Please enter a positive number.")
        return

    if amount > account[5]:
        print("Insufficient balance.")
        return

    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE account_details SET balance = balance - ? WHERE id = ?
    ''', (amount, account[0]))
    conn.commit()
    conn.close()
    print(f"{amount} has been withdrawn from your account. Your new balance is {account[5] - amount}")

def check_balance(account):
    password = getpass.getpass("Enter password: ")

    if password != account[2]:
        print("Incorrect password.")
        return

    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT balance FROM account_details WHERE id = ?
    ''', (account[0],))
    balance = cursor.fetchone()[0]
    conn.close()
    print(f"Current balance: {balance}")

def change_pin(account):
    old_password = getpass.getpass("Enter existing password: ")

    if old_password != account[2]:
        print("Incorrect password.")
        return

    new_password = getpass.getpass("Enter new password: ")
    confirm_password = getpass.getpass("Confirm new password: ")

    if new_password != confirm_password:
        print("Passwords do not match.")
        return

    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE account_details SET password = ? WHERE id = ?
    ''', (new_password, account[0]))
    conn.commit()
    conn.close()
    print("Password changed successfully!")

def view_account_details(account):
    password = getpass.getpass("Enter password: ")

    if password != account[2]:
        print("Incorrect password.")
        return

    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM account_details WHERE id = ?
    ''', (account[0],))
    account_details = cursor.fetchone()
    conn.close()
    print("Account Details:")
    print(f"Username: {account_details[1]}")
    print(f"PAN Card: {account_details[3]}")
    print(f"Nominee Name: {account_details[4]}")
    print(f"Balance: {account_details[5]}")

def deposit_money(account):
    amount = float(input("Enter amount to deposit: "))
    password = getpass.getpass("Enter password: ")

    if password != account[2]:
        print("Incorrect password.")
        return

    if amount <= 0:
        print("Invalid amount. Please enter a positive number.")
        return

    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE account_details SET balance = balance + ? WHERE id = ?
    ''', (amount, account[0]))
    conn.commit()
    conn.close()
    print(f"{amount} has been deposited to your account. Your new balance is {account[5] + amount}")

def main():
    create_database()

    while True:
        print("\nWelcome to the ATM")
        print("1. Create Account")
        print("2. Use Existing Account")
        choice = input("Choose an option: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            username = input("Enter username: ")
            account = check_credentials(username)
            if account:
                while True:
                    print("\n1. Withdraw Money")
                    print("2. Check Balance")
                    print("3. Change PIN")
                    print("4. View Account Details")
                    print("5. Deposit Money")
                    print("q. Quit")
                    action = input("Choose an action: ")

                    if action == '1':
                        withdraw_money(account)
                    elif action == '2':
                        check_balance(account)
                    elif action == '3':
                        change_pin(account)
                    elif action == '4':
                        view_account_details(account)
                    elif action == '5':
                        deposit_money(account)
                    elif action == 'q':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Account not found.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
