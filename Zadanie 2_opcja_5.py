import os
accounts = {}

class Account:
    def __init__(self, username, funds, bank):
        self.username = username
        self.funds = funds
        self.bank = bank
        self.history = []

    def add_history(self, amount, note, from_account=None, to_account=None):
        self.history.append((amount, note, from_account, to_account))
        
class Transaction:
    def io(self, account, amount):
        note = "ATM"
        account.funds += amount
        account.add_history(amount, note)
        
    def transfer(self, from_account, to_account, amount, note):
        from_account.funds -= amount
        to_account.funds += amount
        
        from_account.add_history(-amount, note, from_account, to_account)
        to_account.add_history(amount, note, from_account, to_account)

class Bank:
    def __init__(self, bank):
        self.bank = bank
        
    def calculate_total(self, account):
        return sum(amount for amount, _, _, _ in account.history)
        
def add_user():
    print("> | Dodawanie użytkownika | <")
    username = input("Podaj nazwę posiadacza konta: ")
    bank = Bank(input("Podaj nazwę banku posiadacza konta: "))
    
    account = Account(username, 0.00, bank)
    accounts[username] = account
    
def atm():
    print("> | ATM | <")
    username = input("Podaj nazwę swojego konta: ")
    opt = int(input("1. Wypłata | 2. Wpłata\n"))
    amount = float(input("Podaj kwotę wypłaty/wpłaty do swojego konta: "))
    account = accounts.get(username)
    if opt == 1:
        Transaction().io(account, -amount)
    elif opt == 2:
        Transaction().io(account, amount)
    
def transferto():
    print("> | Transfer | <")
    sender = input("Podaj nazwę swojego konta: ")
    recipient = input("Podaj nazwę konta otrzymującego: ")
    amount = float(input("Podaj kwotę transakcji: "))
    note = input("Opis: ")
    
    sender_acc = accounts.get(sender)
    recipient_acc = accounts.get(recipient)
    Transaction().transfer(sender_acc, recipient_acc, amount, note)
    
def parse_history():
    print("> | Historia transakcji | <")
    username = input("Podaj nazwę swojego konta: ")
    
    account = accounts.get(username)
    clear()

    if not account:
        print("Nie znaleziono konta")
        return
    
    total = sum(amount for amount, _, _, _ in account.history)
    print(f"Środki dla {account.username}: {account.funds} zł")
    print(f"Suma transakcji dla {account.username}: {total} zł")
    print("\n> | Historia transakcji | <")
    
    for amount, note, from_account, to_account in reversed(account.history):
        if from_account and to_account:
            print(f"{amount} zł | {note} | {from_account.username} > {to_account.username}")
        else:
            print(f"{amount} zł | {note}")
            
def parse_account():
    print("> | Lista kont | <\n")
    
    for username, account in accounts.items():
        print(f"Użytkownik: {username}")
        print(f"  Saldo: {account.funds} zł")
        print(f"  Bank: {account.bank.bank}")
        print(f"  Liczba transakcji: {len(account.history)}\n")
            
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    
    # domyślnie wpisane banki i konta, aby kinda pokazać działanie
    ing = Bank("ING")
    mbank = Bank("mBank")
    credit = Bank("Credit")
    
    accounts["Zenek"] = Account("Zenek", 2880.86, ing)
    accounts["Władziu"] = Account("Władziu", 4442.2, credit)
    
    Transaction().io(accounts.get("Zenek"), 1399.99)
    Transaction().io(accounts.get("Władziu"), -1000)
    
    Transaction().transfer(accounts.get("Zenek"), accounts.get("Władziu"), 10, "za podwózkę")
    
    opt = 0
    while opt < 6:
        print(f"> | System bankowy | <")
        opt = int(input("1. Dodaj użytkownika\n2. Wypłać/Wpłać\n3. Wyślij do\n4. Zobacz historię transakcji\n5. Pokaż bazę\n6. Wyjdź\n\nWybierz opcję z podanych: "));
        clear()
        
        match opt:
            case 1:
                add_user()
                input("Wciśnij enter by kontynuować...")
            case 2:
                atm()
                input("Wciśnij enter by kontynuować...")
            case 3:
                transferto()
                input("Wciśnij enter by kontynuować...")
            case 4:
                parse_history()
                input("Wciśnij enter by kontynuować...")
            case 5:
                parse_account()
                input("Wciśnij enter by kontynuować...")
        clear()