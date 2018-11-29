import core.database as database
from bitcoinrpc.authproxy import AuthServiceProxy
from config import kekcoin_rpc_config
import os

# Debug/testing only commands


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

    def create_deposit_address(self, user):
        address = str(user.id) + "deposit"
        self.balances[address] = 100.0
        database.set_deposit_address(user, address)
        return address

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

# END


def get_staking_weight():
    """
    Method used to get Kekcoin steaking info  
    Returns:
            getinfo output (dict)
    """
    rpc = AuthServiceProxy(("http://%s:%s@127.0.0.1:%s/") %
                           (kekcoin_rpc_config['RPC_USER'], kekcoin_rpc_config['RPC_PASS'], kekcoin_rpc_config['RPC_PORT']))

    stakinginfo = rpc.getstakinginfo()
    return '{:,.2f}'.format(float(stakinginfo['netstakeweight']) / 1e8)


def getSubsidy(self, blockcount):
    if blockcount <= 10000:
        return 50
    elif blockcount <= 20000:
        return 25
    elif blockcount <= 30000:
        return 10
    elif blockcount <= 100000:
        return 5
    elif blockcount <= 200000:
        return 2.5
    else:
        return 1


def get_staking_reward():

    rpc = AuthServiceProxy(("http://%s:%s@127.0.0.1:%s/") %
                           (kekcoin_rpc_config['RPC_USER'], kekcoin_rpc_config['RPC_PASS'], kekcoin_rpc_config['RPC_PORT']))

    info = rpc.getinfo()
    stakinginfo = rpc.getstakinginfo()

    return '{:.2f}'.format(100 * (1440 * getSubsidy(int(info['blocks'])) * 365) / (float(stakinginfo['netstakeweight']) / 1e8))


def get_blockchain_size():

    blockchain_size = 0
    for i in range(10):
        if os.path.isfile('/root/.kekcoin/blocks/blk0000%s.dat' % str(i)):
            file_info = os.stat('/root/.kekcoin/blocks/blk0000%s.dat' % str(i))
            file_size = file_info.st_size
            for sizes in ['bytes', 'KB', 'MB', 'GB']:
                if file_size < 1024.0:
                    blockchain_size = "%.1f %s" % (file_size, sizes)
                    break
                file_size /= 1024.0

    return '{}'.format(blockchain_size)


# Returns given user's current KekBot balance as a float
def get_balance(user):

    rpc = AuthServiceProxy(("http://%s:%s@127.0.0.1:%s/") %
                           (kekcoin_rpc_config['RPC_USER'], kekcoin_rpc_config['RPC_PASS'], kekcoin_rpc_config['RPC_PORT']))

    address = database.get_deposit_address(user)

    utxos = rpc.listunspent()
    user_utxos = []
    for utxo in utxos:
        if utxo['address'] == address:
            user_utxos.append(utxo)

    return sum([utxo['amount'] for utxo in user_utxos])

    # return debug.get_balance(user)

# Generates a KekBot deposit address
# Returns deposit address string for use


def create_deposit_address(user):

    rpc = AuthServiceProxy(("http://%s:%s@127.0.0.1:%s/") %
                           (kekcoin_rpc_config['RPC_USER'], kekcoin_rpc_config['RPC_PASS'], kekcoin_rpc_config['RPC_PORT']))

    address = rpc.getnewaddress()

    database.set_deposit_address(user, address)

    return str(address)

    # return debug.create_deposit_address(user)

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
