import core.database as database

### Debug/testing only commands

class WalletDebug():
    def __init__(self):
        self.balances = {}
        users = database.get_users()
        for u in users:
            if u.deposit_address != None:
                self.balances[u.deposit_address] = 100.0

    def add_balance(self, address, amount):
        if address in self.balances:
            self.balances[address] += amount
        else:
            self.balances[address] = amount

    def subtract_balance(self, address, amount):
        if address in self.balances:
            if self.balances[address] - amount >= 0:
                self.balances[address] -= amount
                return True
        return False

    def get_balance(self, user):
        user_model = database.get_user_model(user)
        if user_model == None:
            return False
        if user_model.deposit_address == None:
            return False

        if user_model.deposit_address in self.balances:
            return self.balances[user_model.deposit_address]
        return 0.0

    def make_transaction(self, sender_address, receiver_address, amount):
        self.subtract_balance(sender_address, amount)
        self.add_balance(receiver_address, amount)

    def is_valid_address(self, address):
        return address in self.balances

    def can_withdraw_amount(self, amount, address):
        if address in self.balances:
            return amount <= self.balances[address]
        return False

    def get_withdrawals(self):
        return [
            'one withdrawal',
            'two withdrawal ',
            'three withdrawal',
            'four withdrawal',
            'five withdrawal',
            'six withdrawal',
            'seven withdrawal',
            'eight withdrawal',
            'nine withdrawal',
            'ten withdrawal',
            'eleven withdrawal',
            'twelve withdrawal'
        ]

    def get_deposits(self):
        return [
            'one deposit',
            'two deposit',
            'three deposit',
            'four deposit',
            'five deposit',
            'six deposit',
            'seven deposit',
            'eight deposit',
            'nine deposit',
            'ten deposit',
            'eleven deposit',
            'twelve deposit'
        ]

debug = WalletDebug()

### END

# Returns given user's current KekBot balance as a float
def get_balance(user):
    return debug.get_balance(user)

# Generates a KekBot deposit address
# Returns deposit address string for use
def create_deposit_address(user):
    ### TEMPORARY CODE ###
    address = str(user.id) + "deposit"
    debug.balances[address] = 100.0
    ### TEMPORARY CODE ###
    database.set_deposit_address(user, address)
    return address

# Returns a LIST of transaction ids as strings
def get_withdrawals(address):
    return debug.get_withdrawals()

# Returns a LIST of transaction ids as strings
def get_deposits(address):
    return debug.get_deposits()

# Perform transaction
# Doesn't return anything.  Already wrapped in a try/except block, so should
#    simply throw an exception if failed
def make_transaction(sender_address, receiver_address, amount):
    debug.make_transaction(sender_address, receiver_address, amount)

# Return True if the address is valid to deposit to, else False
# Used for arg-checking commands
def is_valid_address(address):
    return debug.is_valid_address(address)

# Return True if the given address has enough to have amount withdrawn from it,
#    else False
def can_withdraw_amount(amount, address):
    return debug.can_withdraw_amount(amount, address)
