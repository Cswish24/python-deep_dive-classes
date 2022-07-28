from datetime import datetime, timedelta, tzinfo
from numbers import Real
from pytz import timezone
import pytz


class Account:

    interest_rate = 0.005

    _account_ids = list()

    _all_transactions = list()

    def __init__(self, first_name, last_name, timezone_str, balance=50):
        self._id = Account._new_account()
        self._first_name = first_name
        self._last_name = last_name
        self.timezone_str = timezone_str
        self._balance = balance
        self._account_transactions = list()

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def balance(self):
        return self._balance

    @property
    def account_transactions(self):
        return self._account_transactions

    @classmethod
    @property
    def all_transactions(cls):
        return cls._all_transactions

    @classmethod
    @property
    def account_ids(cls):
        return cls._account_ids

    @classmethod
    def _new_account(cls):
        if len(cls._account_ids):
            cls._account_ids.append(cls._account_ids[-1] + 1)
        else:
            cls._account_ids.append(1)
        return cls._account_ids[-1]

    @classmethod
    def _new_transaction_id(cls):
        if len(cls._all_transactions):
            cls._all_transactions.append(cls.all_transactions[-1] + 1)
        else:
            cls._all_transactions.append(1)

        return cls.all_transactions[-1]

    def deposit(self, deposit_amount):
        if isinstance(deposit_amount, Real) and deposit_amount > 0:
            self._balance += deposit_amount
            transaction = Account.Transaction(self, "D")
            self._account_transactions.append(transaction)
            return f"{deposit_amount}$ deposited. Account Balance = {self._balance} $"
        else:
            transaction = Account.Transaction(self, "X")
            self._account_transactions.append(transaction)
            return f"Transaction Denied. Deposit amount must be a positive real number and must be less than the total account balance"

    def withdraw(self, withdraw_amount):
        if isinstance(withdraw_amount, Real) and withdraw_amount > 0 and self._balance > withdraw_amount:
            self._balance -= withdraw_amount
            transaction = Account.Transaction(self, "W")
            self._account_transactions.append(transaction)
            return f"{withdraw_amount}$ withdrawn. Account Balance = {self._balance} $"
        else:
            transaction = Account.Transaction(self, "X")
            self._account_transactions.append(transaction)
            return f"Transaction Denied. Withdraw amount must be a positive real number and must be less than the total account balance"

    def deposit_interest(self):
        interest_accrued = self._balance * Account.interest_rate
        self._balance += interest_accrued
        transaction = Account.Transaction(self, "I")
        self._account_transactions.append(transaction)
        return f"{interest_accrued} $ interest deposited. Account Balance = {self._balance} $"

    def __repr__(self):
        return f"{self.first_name} {self.last_name}'s account\nID = {self._id} \nBalance = {self._balance}$\n"

    class Transaction:

        format = '%Y-%m-%d %H:%M:%S %Z%z'

        def __init__(self, account, code):
            self._id = Account._new_transaction_id()
            self._account_id = account._id
            self._transaction_code = code
            self.timezone_str = account.timezone_str
            self._time = Account.Transaction._transaction_time(
                self.timezone_str)

        @classmethod
        def _transaction_time(cls, timezone_str):
            utc = pytz.utc
            now = datetime.now(utc)
            tz_object = timezone(timezone_str)
            loc_dt = now.astimezone(tz_object)
            return loc_dt.strftime(cls.format)

        def __repr__(self):
            return f"\nAccount ID: {self._account_id}\nTransaction ID: {self._id}\nTransaction Type: {self._transaction_code}\nTime: {self._time}\n"


acc = Account('cboy', 'bboy', "US/Central")
acc2 = Account('ddd', 'ffdf', "US/Mountain")

print(acc)
print(acc2)

print(acc.deposit(100))
print(acc.withdraw(1000))
print(acc2.deposit(100))
print(acc.withdraw(2))
print(acc.deposit(-1))
print(acc)
transactions = Account.all_transactions
print(transactions)

print(acc.account_transactions)
print(acc2.account_transactions)

ids = Account.account_ids
print(len(ids))

tests = [acc.balance, acc.first_name, acc.last_name,
         acc.full_name, acc.timezone_str, acc.deposit_interest()]

print(tests)

acc.first_name = 'Bob'
acc.last_name = 'Dylanger'
acc.timezone_str = "US/Pacific"

tests = [acc.balance, acc.first_name, acc.last_name,
         acc.full_name, acc.timezone_str, acc.deposit_interest()]
print(tests)
print(acc.account_transactions)
