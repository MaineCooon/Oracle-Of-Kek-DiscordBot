from abc import ABC, abstractmethod
import requests
from io import BytesIO

from pprint import pprint
from inspect import getmembers

from core.command import *

import core.database as database
import templates
import config

# Parent class for all !add commands
class AddCommand(Command, ABC):

    def __init__(self, client):
        super().__init__(client)
        self.timeout = config.add_row_timeout # Add timeout to class properties

    @property
    @abstractmethod
    def _await_message(self):
        pass

    @abstractmethod
    def _is_valid_submission(self, msg):
        pass

    @abstractmethod
    def _submit_to_database(self, msg):
        pass

    @abstractmethod
    async def _display_submission(self, msg):
        pass

    @property
    def _add_cancelled_message(self):
        return templates.add_cancelled_message

    # All !add commands require admin privileges
    def check_privs(self, discord_user):
        return database.is_admin(discord_user)

    async def execute(self, msg, args):
        channel = msg.channel

        # Ask user to send new submission

        await self.client.send_typing(channel)
        await self.client.send_message(channel, self._await_message)

        # Wait for next message from user (with a timeout period set in config)

        response = await self.client.wait_for_message(timeout=config.add_row_timeout, author=msg.author)

        if response == None:
            # If no message was sent before timeout ended, abort
            await self.client.send_typing(channel)
            await self.client.send_message(channel, templates.add_cancelled_message)
            return
        elif response.content.lower() == "stop":
            # If user sent 'stop', exit
            await self.client.send_typing(channel)
            await self.client.send_message(channel, templates.add_stopped_message)
            return

        # Verify submission is valid for submission type

        if not self._is_valid_submission(response):
            # If what they submitted isn't valid, such as submitting an image
            #    for 'advice', text for 'gif', etc., exit
            await self.client.send_typing(channel)
            await self.client.send_message(channel, templates.invalid_submission_message)
            return

        # If database submission double-confirmation is turned on...
        if config.confirm_database_submissions:
            # Verify with user this is what they want to submit
            repost = await self._display_submission(response)
            await self.client.send_typing(channel)
            confirmation = await self.client.send_message(channel, templates.confirm_submission_message)

            # Create reaction options
            await self.client.add_reaction(confirmation, templates.yes_emoji)
            await self.client.add_reaction(confirmation, templates.no_emoji)

            # Wait for user to select one
            res = await self.client.wait_for_reaction(
                emoji = [templates.yes_emoji, templates.no_emoji],
                user = msg.author,
                timeout = config.confirm_reaction_timeout
            )

            if res.reaction.emoji == templates.yes_emoji:
                await self.client.delete_message(repost)
                await self.client.clear_reactions(confirmation)
                await self.client.edit_message(confirmation, templates.pending_submission_message)
            elif res.reaction.emoji == templates.no_emoji:
                await self.client.delete_message(repost)
                await self.client.clear_reactions(confirmation)
                await self.client.edit_message(confirmation, templates.submission_cancelled_message)
                return
            else:
                await self.client.send_typing(channel)
                await self.client.send_message(channel, templates.try_again_message)
                return

        send = templates.submission_complete_message
        try:
            # Try adding submission to database
            self._submit_to_database(response)
        except:
            # If it failed, say so
            send = templates.submission_failed_message

        await self.client.edit_message(confirmation, send)



            # url = response.attachments[0]['url']
            # img = requests.get(url).content
            # database.add_meme(msg.author, url)
            # await self.client.send_file(channel, BytesIO(img), filename="meme.png")


# TODO probably needs cleanup later
@command
class AddKekCommand(Command):
    name = "addkek"
    description = "add kek quote"

    def check_privs(self, discord_user):
        return database.is_admin(discord_user)

    async def execute(self, msg, args):
        await self.client.send_message(msg.channel, templates.await_kek_message.format(user=msg.author.display_name))
        response = await self.client.wait_for_message(timeout=config.add_row_timeout, author=msg.author)
        if response == None:
            await self.client.send_message(msg.channel, templates.add_kek_cancelled_message)
            return
        elif response.content.lower() == "stop":
            await self.client.send_message(msg.channel, "Stopped.  :P")
            return

        # TODO Add second check where user can verify quote is correct
        database.add_kek(msg.author, response.content)
        await self.client.send_message(msg.channel, "Added kek '{kek}'".format(kek=response.content))
        # if len(args) < 1:
        #     await self.client.send_message(msg.channel, "Must have args")
        #     return
        #
        # submission = " ".join(args)
        # database.add_kek(msg.author, submission)
        # await self.client.send_message(msg.channel, "Added!")

@command
class AddMemeCommand(AddCommand):
    name = "addmeme"
    description = "add meme"

    _await_message = "awaiting meme"

    def _is_valid_submission(self, msg):
        return True

    def _submit_to_database(self, msg):
        url = msg.attachments[0]['url']
        database.add_meme(msg.author, url)
        # url = response.attachments[0]['url']
        # img = requests.get(url).content
        # database.add_meme(msg.author, url)
        # await self.client.send_file(channel, BytesIO(img), filename="meme.png")

    async def _display_submission(self, msg):
        url = msg.attachments[0]['url']
        img = requests.get(url).content
        # database.add_meme(msg.author, url)
        return await self.client.send_file(msg.channel, BytesIO(img), filename="meme.png")

    # async def execute(self, msg, args):
    #     # TODO implement !addmeme
    #     await self.client.send_message(msg.channel, "Coming soon...")

@command
class AddGifCommand(Command):
    name = "addgif"
    description = "add gif"

    async def execute(self, msg, args):
        # TODO implement !addgif
        await self.client.send_message(msg.channel, "Coming soon...")

@command
class AddAdviceCommand(Command):
    name = "addadvice"
    description = "add advice"

    async def execute(self, msg, args):
        # TODO implement !addadvice
        await self.client.send_message(msg.channel, "Coming soon...")

@command
class AddTrumpCommand(Command):
    name = "addtrump"
    description = "add trump"

    async def execute(self, msg, args):
        # TODO implement !addtrump
        await self.client.send_message(msg.channel, "Coming soon...")
