# main.py
from src.customer import Customer
from decimal import Decimal
import json
import os
import sys
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\n=== Welcome to Sammy-PyBank ===")
    print("1. Create Account")
    print("2. Login")
    print("3. Check Balance")
    print("4. Deposit")
    print("5. Withdraw")
    print("6. Transfer")
    print("7. Transaction History")
    print("8. Exit")
    return input("\nSelect an option: ")

    customers = {}
    try:
        with open("./data/customers.json", "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    try:
                        customer = Customer(
                            first_name=data['first_name'],
                            last_name=data['last_name'],
                            email=data['email'],
                            phone=data['phone'],
                            address=data['address'],
                            customer_id=data['customer_id'],
                            account_number=data['account_number'],
                            password=data['password'],
                            transaction_pin=data['transaction_pin'],
                            is_logged_in=data['is_logged_in'],
                            balance=Decimal(str(data.get('balance', '0.00'))),
                            transactions=data.get('transactions', [])
                        )
                        customers[customer.email] = customer
                    except KeyError as ke:
                        print(f"Missing required field in customer data: {ke}")
                        continue
                    except ValueError as ve:
                        print(f"Invalid data format: {ve}")
                        continue
                except json.JSONDecodeError as je:
                    print(f"Invalid JSON format in line: {je}")
                    continue
    except FileNotFoundError:
        print("Customers file not found. Creating new database.")
        # Create the data directory if it doesn't exist
        os.makedirs("./data", exist_ok=True)
        # Create empty customers file
        with open("./data/customers.json", "w") as f:
            pass
    except PermissionError:
        print("Error: No permission to access customers file")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error loading customers: {e}")
        sys.exit(1)
    
    return customers

def generate_account_number(customers):
    # 8 digit account number
    account_number = f"ACC{len(customers) + 1:08d}"
    return account_number

def main():
    customers = {} 
    current_user = None
    
    # load customers from json file
    # customers = load_customers()
    # customrs = {}
            
    
    while True:
        clear_screen()
        if not current_user:
            print("Please login or create an account")
        else:
            print(f"Welcome, {current_user.first_name}")
            
        choice = display_menu()
        
        if choice == '1':
            # Create Account
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            address = input("Enter address: ")
            password = input("Create password: ")
            
            customer_id = f"CUST{len(customers) + 1:03d}"
            account_number = generate_account_number(customers)
            
            new_customer = Customer(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                customer_id=customer_id,
                password=password,
                account_number=account_number,
            )
            customers[email] = new_customer
            print("Account created successfully!")
            print(f"Your account number is: {account_number}")
            
            # store user creation in a json file
            # with open("./data/customers.json", "a") as f:
            #     f.write(json.dumps(new_customer.__dict__) + "\n")
            
        elif choice == '2':
            # Login
            email = input("Enter email: ")
            password = input("Enter password: ")
            
            if email in customers and customers[email].password == password:
                current_user = customers[email]
                current_user.is_logged_in = True
                print("Login successful!")
            else:
                print("Invalid credentials!")
                
        elif choice == '3' and current_user:
            # Check Balance
            
            print(f"Current balance: ${current_user.get_balance()}")
            
        elif choice == '4' and current_user:
            # Deposit
            amount = Decimal(input("Enter amount to deposit (in numbers): "))
            current_user.deposit(amount)
            print("Deposit successful!")
            
        elif choice == '5' and current_user:
            # Withdraw
            amount = Decimal(input("Enter amount to withdraw (in numbers): "))
            try:
                current_user.withdraw(amount)
                print("Withdrawal successful!")
            except ValueError as e:
                print(e)
                
        elif choice == '6' and current_user:
            # Transfer
            recipient_account_number = input("Enter recipient account number: ")
            amount = Decimal(input("Enter amount to transfer (in numbers): "))
            recipient = None
            for customer in customers.values():
                if customer.account_number == recipient_account_number:
                    recipient = customer
                    break
            if recipient:
                current_user.transfer(amount, recipient)
                print("Transfer successful!")
            else:
                print("Recipient not found!")
            
                
        
        elif choice == '7' and current_user:
            # Transaction History
            print("Transaction History")
            for transaction in current_user.transactions:
                print(transaction)
        
        elif choice == '8':
            print("Thank you for using Sammy-PyBank!")
            break
            
        else:
            if not current_user:
                print("Please login first!")
            else:
                print("Invalid option!")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()