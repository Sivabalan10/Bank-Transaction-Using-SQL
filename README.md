# Bank-Transaction-Using-SQL
This project is a Python-based ATM simulation system that performs basic banking transactions. It uses SQLite as the database to store and manage account details. This mini project was developed for my academic coursework in database management systems.

## Features

1. **Create Account**: 
    - Users can create a new account by providing their username, password, PAN card number, nominee name, and initial balance.
    - The initial balance is set to 1000 by default.

2. **Existing Account**:
    - Users can log in to their existing account by providing their username.
    - After logging in, users can:
        - Withdraw Money
        - Check Balance
        - Change PIN
        - View Account Details
        - Deposit Money

## Code Explanation

- **Database Setup**: The `create_database()` function ensures the `account_details` table exists.
- **Creating an Account**: The `create_account()` function stores user details in the database.
- **Checking Credentials**: The `check_credentials()` function verifies if a username exists.
- **Withdrawing Money**: The `withdraw_money()` function handles money withdrawal after password verification.
- **Checking Balance**: The `check_balance()` function displays the balance after password verification.
- **Changing PIN**: The `change_pin()` function changes the password after verifying the existing password.
- **Viewing Account Details**: The `view_account_details()` function shows account details after password verification.
- **Depositing Money**: The `deposit_money()` function handles money deposits after password verification.

## How to Run

1. **Clone the Repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Ensure you have Python installed**:
    - Download Python from [python.org](https://www.python.org/).

3. **Run the Script**:
    ```sh
    python main.py
    ```

4. **Follow the On-Screen Instructions**:
    - Create a new account or log in to an existing account.
    - Perform actions like withdrawing money, checking balance, changing PIN, viewing account details, and depositing money.

## Developed as a Mini Project

This project was developed as a mini project for my academic coursework in database management systems. It showcases the integration of Python programming with SQLite for handling basic banking transactions in a simulated ATM environment.
