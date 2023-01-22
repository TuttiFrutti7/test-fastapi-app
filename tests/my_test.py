import pytest
from app.fuck import calc, minus, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(21)

@pytest.mark.parametrize("a, b, result", [
    (1,2,3),
    (2,5,7),
    (9,9,18)
])
def test_calc(a, b, result):
    assert calc(a,b) == result

def test_minus():
    assert minus(8, 5) == 3

def test_bank_set_initial_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(9)
    assert bank_account.balance == 12

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert bank_account.balance == 23.1

@pytest.mark.parametrize("deposit, withdraw, balance", [
    (21, 2, 19),
    (2000, 1500, 500),
    (0.27, 0.02, 0.25)
])
def test_bank_transaction(zero_bank_account, deposit, withdraw, balance):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == balance

def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(50)