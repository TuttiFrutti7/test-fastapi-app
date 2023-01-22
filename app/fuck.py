def calc(a: int, b: int):
    return a+b

def minus(a: int, b: int):
    return a-b

class InsufficientFunds(Exception):
    pass

class BankAccount:
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Not enough money")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1