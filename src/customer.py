from typing import List
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from numbers import Number

@dataclass
class Customer:
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    customer_id: str
    account_number: int
    # created_at: datetime = field(default_factory=datetime.now)
    # login details
    password: str = None
    transaction_pin: str = None
    is_logged_in: bool = False
    balance: Decimal = field(default=Decimal('0.00'))
    transactions: List[dict] = field(default_factory=list)
    
    
    def create_transaction_pin(self, pin: Number, confirm_pin: Number) -> None:
        if (len(pin) != 4):
            print("PIN TO LONG. SHOULD BE 4 DIGITS")
        if pin != confirm_pin:
            print("PINS DO NOT MATCH")
        else:
            self.transaction_pin = pin
            print("PIN SET SUCCESSFULLY")
            
    def create_password(self, password: str, confirm_password: str) -> None:
        if password != confirm_password:
            print("PASSWORDS DO NOT MATCH")
        else:
            self.password = password
            print("PASSWORD SET SUCCESSFULLY")
            
    def login(self, password: str) -> bool:
        if password == self.password:
            self.is_logged_in = True
            return True
        return False
    
    def deposit(self, amount: Decimal) -> None:
        self.balance += amount
        self.transactions.append({
            'type': 'deposit',
            'amount': amount,
            'timestamp': datetime.now()
        })

    def withdraw(self, amount: Decimal) -> None:
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append({
                'type': 'withdrawal',
                'amount': amount,
                'timestamp': datetime.now()
            })
        else:
            raise ValueError("Insufficient funds")

    def transfer(self, amount: Decimal, recipient: 'Customer') -> None:
        if self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            self.transactions.append({
                'type': 'transfer',
                'amount': amount,
                'to': recipient.email,
                'timestamp': datetime.now()
            })
            recipient.transactions.append({
                'type': 'transfer',
                'amount': amount,
                'from': self.email,
                'timestamp': datetime.now()
            })
        else:
            raise ValueError("Insufficient funds")
        
    def get_balance(self) -> Decimal:
        return self.balance
    
    def get_transactions(self) -> List[dict]:
        return self.transactions
    
