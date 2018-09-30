import requests
from abc import ABC, abstractmethod
from io import BytesIO
from discord import MessageType

import core.database as database
import templates
import config
from core.command import *

# Parent class for all !add commands
class AddCommand(Command, ABC):

    @abstractmethod
    def _is_valid_submission(self, msg):
        pass

    @abstractmethod
    def _submit_to_database(self, msg):
        pass

    @abstractmethod
    async def _display_submission(self, msg):
        pass

    # All !add commands require admin privileges
    def check_privs(self, discord_user):
        return database.is_admin(discord_user)

    async def execute(self, msg, args):
        channel = msg.channel

        # Ask user to send new submission

        await self.client.send_typing(channel)
        await self.client.send_message(channel, templates.await_submission_message)

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

        try:
            await self.client.edit_message(confirmation, send)
        except:
            # If confirmation is turned off, a new message will need to be
            #    sent instead of editing the old one
            await self.client.send_message(msg.channel, send)


# TODO probably needs cleanup later
@command
class AddKekCommand(AddCommand):
    name = "addkek"
    description = "add kek quote"

    def _is_valid_submission(self, msg):
        return msg.type == MessageType.default and len(msg.content) > 0

    def _submit_to_database(self, msg):
        database.add_kek(msg.author, msg.content)

    async def _display_submission(self, msg):
        return await self.client.send_message(msg.channel, msg.content)


@command
class AddMemeCommand(AddCommand):
    name = "addmeme"
    description = "add meme"

    def _is_valid_submission(self, msg):
        try:
            # Make sure submission includes an image
            url = msg.attachments[0]['url']
        except:
            return False
        return True

    def _submit_to_database(self, msg):
        url = msg.attachments[0]['url']
        database.add_meme(msg.author, url)

    async def _display_submission(self, msg):
        url = msg.attachments[0]['url']
        img = requests.get(url).content
        return await self.client.send_file(msg.channel, BytesIO(img), filename="meme.png")

@command
class AddGifCommand(AddCommand):
    name = "addgif"
    description = "add gif"

    def _is_valid_submission(self, msg):
        try:
            # Make sure submission includes an image
            url = msg.attachments[0]['url']
        except:
            return False
        return True

    def _submit_to_database(self, msg):
        url = msg.attachments[0]['url']
        # TODO these database submission functions need try/catch wrappers
        database.add_gif(msg.author, url)

    async def _display_submission(self, msg):
        url = msg.attachments[0]['url']
        img = requests.get(url).content
        return await self.client.send_file(msg.channel, BytesIO(img), filename="gif.gif")


@command
class AddAdviceCommand(AddCommand):
    name = "addadvice"
    description = "add advice"

    def _is_valid_submission(self, msg):
        return msg.type == MessageType.default and len(msg.content) > 0

    def _submit_to_database(self, msg):
        database.add_advice(msg.author, msg.content)

    async def _display_submission(self, msg):
        return await self.client.send_message(msg.channel, msg.content)


@command
class AddTrumpCommand(AddCommand):
    name = "addtrump"
    description = "add trump"

    def _is_valid_submission(self, msg):
        return msg.type == MessageType.default and len(msg.content) > 0

    def _submit_to_database(self, msg):
        database.add_trump(msg.author, msg.content)

    async def _display_submission(self, msg):
        return await self.client.send_message(msg.channel, msg.content)
