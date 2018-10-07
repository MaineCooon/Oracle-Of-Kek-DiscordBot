import random
from discord import ChannelType, Embed

import config
import core.database as database
import templates as t
import core.wallet as wallet
from core.command import *

# TODO DEBUG COMMAND FOR TESTING.  REMOVE LATER.
@command
class AddBalanceCommand(Command):
    name = "addbalance"
    description = "aisjdf"
    usage = f"`{config.prefix}addbalance`"

    def check_privs(self, discord_user):
        return database.is_admin(discord_user)

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)
        user = msg.mentions[0]
        amount = float(args[1])
        address = database.get_deposit_address(user)
        try:
            wallet.debug.add_balance(address, amount)
        except:
            await self.client.send_message(msg.channel, "WRITE BETTER COMMANDS")
            return
        await self.client.send_typing(msg.channel)
        await self.client.send_message(msg.channel, "Balance added!")

@command
class RegisterCommand(Command):
    name = "register"
    description = "Registers user a tipping account with the bot."
    usage = f"`{config.prefix}register`"

    def check_channel_type(self, channel):
        # Only work in DMs
        return channel.is_private

    async def execute(self, msg, args):
        user_model = database.get_or_make_user_model(msg.author)
        await self.client.send_typing(msg.channel)

        # Check if user has already had an account/deposit address saved
        if user_model.deposit_address != None:
            await self.client.send_message(msg.channel,
                t.tipping_account_exists_message.format(prefix=config.prefix, username_tag=msg.author.mention)
            )
            return

        # If not, proceed to make one

        try:
            address = wallet.create_deposit_address(msg.author)
        except:
            await self.client.send_message(msg.channel, t.tipping_account_creation_failed_message)

        # Announce new account to user
        await self.client.send_message(msg.channel,
            t.tipping_account_created_message.format(username_tag=msg.author.mention)
        )

@command
class BalanceCommand(Command):
    name = "balance"
    description = "Displays current KekBot tipping account balance."
    usage = f"`{config.prefix}balance`"

    def check_channel_type(self, channel):
        # Only work in DMs
        return channel.is_private

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        # Check if user has account registered
        if not database.has_tip_account(msg.author):
            # If not, tell them so and abort
            await self.client.send_message(msg.channel,
                t.no_tipping_account_exists_message(username_tag=msg.author.mention, prefix=config.prefix)
            )
            return

        # Else, retrieve their balance using their saved address
        balance = wallet.get_balance(msg.author)

        # If balance retrieval somehow failed
        if type(balance) is not float and type(balance) is not int:
            await self.client.send_message(msg.channel,
                t.balance_unavailable_message.format(username_tag=msg.author.mention)
            )
            return

        # Announce balance to user
        balance_string = "{0:.2f}".format(balance)
        await self.client.send_message(msg.channel, t.display_balance_message.format(balance=balance_string))

@command
class DepositCommand(Command):
    name = "deposit"
    description = "Shows tipping account deposit address."
    usage = f"`{config.prefix}deposit`"

    def check_channel_type(self, channel):
        # Only work in DMs
        return channel.is_private

    async def execute(self, msg, args):
        deposit_address = database.get_deposit_address(msg.author)
        await self.client.send_typing(msg.channel)

        # Check if user has account registered
        if deposit_address == False or deposit_address == None:
            # If not, tell them so and abort
            await self.client.send_message(msg.channel,
                t.no_tipping_account_exists_message.format(username_tag=msg.author.mention, prefix=config.prefix)
            )
            return

        # Else, announce their deposit address to them
        await self.client.send_message(msg.channel, deposit_address)

@command
class WithdrawCommand(Command):
    name = "withdraw"
    description = "Withdraws from tipping account to address."
    usage = f"`{config.prefix}withdraw <address> <amount>`"

    def check_channel_type(self, channel):
        # Only work in DMs
        return channel.is_private

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        # Ensure proper argument amount
        if len(args) != 2:
            await self.client.send_message(msg.channel, t.usage_message.format(usage=self.usage))
            return
        address = args[0]
        amount = args[1]

        # Ensure provided receiving address is valid
        if not wallet.is_valid_address(address):
            await self.client.send_message(msg.channel, t.invalid_address_message)
            return

        # Ensure the user of the command has a registered tipping account
        sender_address = database.get_deposit_address(msg.author)
        if sender_address == False:
            await self.client.send_message(msg.channel,
                t.no_tipping_account_exists_message.format(username_tag=msg.author.mention, prefix=config.prefix)
            )
            return

        # Ensure provided amount is a valid float number
        try:
            amount = float(amount)
        except:
            await self.client.send_message(msg.channel, t.usage_message.format(usage=self.usage))
            return

        # Ensure user has enough funds to withdraw specified amount
        if not wallet.can_withdraw_amount(amount, sender_address):
            await self.client.send_message(msg.channel, t.cant_withdraw_amount_message)
            return

        # Finally, perform withdrawal
        try:
            wallet.make_transaction(sender_address, address, amount)
        except:
            # If it failed, say so
            await self.client.send_message(msg.channel, t.withdrawal_failed_message)
            return

        # Announce completed withdrawal
        await self.client.send_message(msg.channel, t.withdrawal_completed_message)

@command
class TipCommand(Command):
    name = "tip"
    description = "Tip KekCoins to another user."
    usage = f"`{config.prefix}tip @<user> <amount>`"

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        # Ensure proper argument amount
        if len(args) != 2:
            await self.client.send_message(msg.channel, t.usage_message.format(usage=self.usage))
            return
        user_tag = args[0]
        amount = args[1]

        # Ensure valid user tag
        if len(msg.mentions) != 1:
            await self.client.send_message(msg.channel, t.usage_message.format(usage=self.usage))
            return
        if msg.mentions[0].mention.replace('!', '') != user_tag.replace('!', ''): # Tags sometimes have ! in them
            await self.client.send_message(msg.channel, t.usage_message.format(usage=self.usage))
            return

        # print(msg.mentions[0].mention)
        # print(user_tag)

        # Set receiving user
        receiver = msg.mentions[0]

        # Ensure provided amount is a valid float number
        try:
            amount = float(amount)
        except:
            await self.client.send_message(msg.channel, t.usage_message.format(usage=self.usage))
            return

        # Ensure the user of the command has a registered tipping account
        sender_address = database.get_deposit_address(msg.author)
        if sender_address == False:
            await self.client.send_message(msg.channel,
                t.no_tipping_account_exists_message.format(username_tag=msg.author.mention, prefix=config.prefix)
            )
            return

        # Ensure user has enough funds to withdraw specified amount
        if not wallet.can_withdraw_amount(amount, sender_address):
            await self.client.send_message(msg.channel, t.cant_withdraw_amount_message)
            return

        # Ensure the receiver has a registered tipping account
        receiver_address = database.get_deposit_address(receiver)
        if receiver_address == False:
            await self.client.send_message(msg.channel,
                t.no_tipping_account_exists_message.format(username_tag=receiver.mention, prefix=config.prefix)
            )
            return

        # Finally, perform withdrawal
        try:
            wallet.make_transaction(sender_address, receiver_address, amount)
        except:
            # If it failed, say so
            await self.client.send_message(msg.channel, t.tip_failed_message)
            return

        # Add tip to database
        database.add_tip(msg.author, receiver, amount)

        # Announce completed tip
        await self.client.send_message(msg.channel, t.tip_completed_message)

@command
class DepositsCommand(Command):
    name = "deposits"
    description = "Displays deposit history of tipping account."
    usage = f"`{config.prefix}deposits`"

    def check_channel_type(self, channel):
        # Only work in DMs
        return channel.is_private

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        # Ensure the user of the command has a registered tipping account
        address = database.get_deposit_address(msg.author)
        if address == False:
            await self.client.send_message(msg.channel,
                t.no_tipping_account_exists_message.format(username_tag=msg.author.mention, prefix=config.prefix)
            )
            return

        try:
            deposits = wallet.get_deposits(address)
            if type(deposits) is list:
                if len(deposits) > 0:
                    # All information retrieved correctly, display list
                    await self.client.send_message(msg.channel,
                        t.deposit_history_message.format(
                            deposits='\n'.join(deposits[:config.deposits_list_limit])
                        )
                    )
                    return
        except:
            pass

        # Code falls down here if anything failed - announce failure
        await self.client.send_message(msg.channel, t.list_deposits_failed_message)

@command
class WithdrawalsCommand(Command):
    name = "withdrawals"
    description = "Displays withdrawal history of tipping account."
    usage = f"`{config.prefix}withdrawals`"

    def check_channel_type(self, channel):
        # Only work in DMs
        return channel.is_private

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        # Ensure the user of the command has a registered tipping account
        address = database.get_deposit_address(msg.author)
        if address == False:
            await self.client.send_message(msg.channel,
                t.no_tipping_account_exists_message.format(username_tag=msg.author.mention, prefix=config.prefix)
            )
            return

        try:
            withdrawals = wallet.get_withdrawals(address)
            if type(withdrawals) is list:
                if len(withdrawals) > 0:
                    # All information retrieved correctly, display list
                    await self.client.send_message(msg.channel,
                        t.withdrawal_history_message.format(
                            withdrawals='\n'.join(withdrawals[:config.withdrawals_list_limit])
                        )
                    )
                    return
        except:
            pass

        # Code falls down here if anything failed - announce failure
        await self.client.send_message(msg.channel, t.list_withdrawals_failed_message)

@command
class TipsCommand(Command):
    name = "tips"
    description = "Displays tipping history of tipping account, both sent and received."
    usage = f"`{config.prefix}tips`"

    def check_channel_type(self, channel):
        # Only work in DMs
        return channel.is_private

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        # Ensure the user of the command has a registered tipping account
        user_address = database.get_deposit_address(msg.author)
        if user_address == False:
            await self.client.send_message(msg.channel,
                t.no_tipping_account_exists_message.format(username_tag=msg.author.mention, prefix=config.prefix)
            )
            return

        tips = database.get_tips_by_user(msg.author)
        given = tips['given']
        received = tips['received']

        given_strings = []
        received_strings = []

        for tip in given[:config.tip_list_limit]:
            given_strings.append(t.list_sent_tips.format(
                username_tag = "<@!{}>".format(tip.receiver_discord_id),
                amount = "{0:.2f}".format(tip.amount)
            ))
        for tip in received[:config.tip_list_limit]:
            received_strings.append(t.list_received_tips.format(
                username_tag = "<@!{}>".format(tip.tipper_discord_id),
                amount = "{0:.2f}".format(tip.amount)
            ))

        if not len(given_strings) > 0:
            given_string = "None"
        else:
            given_string = '\n'.join(given_strings)

        if not len(received_strings) > 0:
            received_string = "None"
        else:
            received_string = '\n'.join(received_strings)

        embed = Embed(
            title = "Tipping History",
            color = config.embed_color
        ).add_field(
            name = "Sent:",
            value = given_string
        ).add_field(
            name = "Received:",
            value = received_string
        )

        try:
            await self.client.send_message(msg.channel, embed=embed)
        except:
            await self.client.send_message(msg.channel, t.list_tips_failed_message)

@command
class BetCommand(Command):
    name = "bet"
    description = "Bet your coins and try your luck!"
    usage = f"`{config.prefix}bet <amount>`"

    def __init__(self, client):
        super().__init__(client)
        address = database.get_deposit_address(client.user)
        if address == False:
            address = wallet.create_deposit_address(client.user)
        self.bot_address = address

    def _generate_number_array(self):
        nums = []
        for i in range(7):
            nums.append(random.randint(0, 9))
        return nums

    # Returns the number of matching numbers at the end of the array as an int
    #    If no match, this will be 0
    def _check_match(self, number_array):
        arr = number_array
        if arr[-2:-1] == arr[-1:]:
            if arr[-3:-2] == arr[-1:]:
                if arr[-4:-3] == arr[-1:]:
                    return 4
                else:
                    return 3
            return 2
        else:
            return 0

    async def execute(self, msg, args):
        await self.client.send_typing(msg.channel)

        # Ensure proper argument amount
        if len(args) != 1:
            await self.client.send_message(msg.channel, t.usage_message.format(usage=self.usage))
            return
        amount = args[0]

        # Ensure provided amount is a valid float number
        try:
            amount = float(amount)
        except:
            await self.client.send_message(msg.channel, t.usage_message.format(usage=self.usage))
            return

        # Ensure the user of the command has a registered tipping account
        address = database.get_deposit_address(msg.author)
        if address == False:
            await self.client.send_message(msg.channel,
                t.no_tipping_account_exists_message.format(username_tag=msg.author.mention, prefix=config.prefix)
            )
            return

        # Ensure user has enough funds to bet specified amount
        if not wallet.can_withdraw_amount(amount, address):
            await self.client.send_message(msg.channel, t.cant_bet_amount_message)
            return

        # Finally, place bet

        number_array = self._generate_number_array()
        matches = self._check_match(number_array)

        send = ''.join([str(num) for num in number_array])
        payout = 0

        if matches == 2:
            payout = amount * config.bet_payout_dubs
            send = t.announce_dubs_message.format(number=send, payout=payout)
        elif matches == 3:
            payout = amount * config.bet_payout_trips
            send = t.announce_trips_message.format(number=send, payout=payout)
        elif matches == 4:
            payout = amount * config.bet_payout_quads
            send = t.announce_quads_message.format(number=send, payout=payout)

        try:
            if matches == 0:
                # If they didn't win, subtract their bet from their account
                wallet.make_transaction(address, self.bot_address, amount)
            else:
                # If they DID win, add their payout to their account
                wallet.make_transaction(self.bot_address, address, payout)
        except:
            # On the off-chance something went wrong, say so and abort
            await self.client.send_message(msg.channel, t.bet_failed_message)

        await self.client.send_message(msg.channel, send)
