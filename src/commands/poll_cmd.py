from asyncio import sleep
from discord import Embed, MessageType, ChannelType

import config
import templates as t
import core.database as database
from core.command import *
from core.poll import *

active_polls = []

def is_message_active_poll(msg):
    for p in active_polls:
        if msg.id == p['message'].id:
            return True
    return False

async def process_poll_reaction(reaction, user, client):
    # Fetch which poll the reaction is on
    poll = None
    poll_message = None
    for p in active_polls:
        if reaction.message.id == p['message'].id:
            poll, poll_message = p['poll'], p['message']
    if poll == None or poll_message == None:
        return

    # If the reaction's not a valid vote, abort
    if not reaction.emoji in poll.get_emoji_array():
        return

    # If the reaction was sent by a bot (including this bot), abort
    if user.bot:
        return

    # Add vote to poll object and remove reaction from the post
    poll.add_vote(user, t.number_emojis.index(reaction.emoji))
    await client.remove_reaction(poll_message, reaction.emoji, user)

@command
class PollCommand(Command):
    name = "poll"
    description = "Create a poll for users to vote on."
    usage = f"`{config.prefix}poll`"
    selection_limit = 10

    def check_privs(self, discord_user):
        return database.is_admin(discord_user)

    def check_channel_type(self, channel):
        return not channel.is_private

    async def _prompt_question(self, msg):
        channel = msg.channel

        # Ask user to send new submission

        await self.client.send_typing(channel)
        await self.client.send_message(channel, t.await_question_message)

        # Wait for next message from user (with a timeout period set in config)

        response = await self.client.wait_for_message(
            timeout = config.create_question_timeout,
            channel = msg.channel,
            author = msg.author
        )

        if response == None:
            # If no message was sent before timeout ended, abort
            await self.client.send_typing(channel)
            await self.client.send_message(channel, t.create_question_cancelled_message)
            return False
        elif response.content.lower() == "stop":
            # If user sent 'stop', exit
            await self.client.send_typing(channel)
            await self.client.send_message(channel, t.create_question_stopped_message)
            return False

        # Verify response message is valid

        if not msg.type == MessageType.default and len(msg.content) > 0:
            # If not, exit
            await self.client.send_typing(channel)
            await self.client.send_message(channel, t.invalid_question_message)
            return False

        new_question = response.content

        # If poll creation double-confirmation is turned on...
        if config.confirm_poll_creation:
            # Verify with user this is what they want to submit
            repost = await self.client.send_message(channel, new_question)
            await self.client.send_typing(channel)
            confirmation = await self.client.send_message(channel, t.confirm_question_message)

            # Create reaction options
            await self.client.add_reaction(confirmation, t.yes_emoji)
            await self.client.add_reaction(confirmation, t.no_emoji)

            # Wait for user to select one
            res = await self.client.wait_for_reaction(
                message = confirmation,
                emoji = [t.yes_emoji, t.no_emoji],
                user = msg.author,
                timeout = config.confirm_reaction_timeout
            )

            if res == None:
                await self.client.delete_message(repost)
                await self.client.clear_reactions(confirmation)
                await self.client.edit_message(confirmation, t.confirm_reaction_timeout_message)
                return False

            if res.reaction.emoji == t.yes_emoji:
                await self.client.delete_message(repost)
                try:
                    await self.client.clear_reactions(confirmation)
                except:
                    pass
            elif res.reaction.emoji == t.no_emoji:
                await self.client.delete_message(repost)
                await self.client.clear_reactions(confirmation)
                await self.client.edit_message(confirmation, t.create_poll_cancelled_message)
                return False
            else:
                await self.client.send_typing(channel)
                await self.client.send_message(channel, t.try_again_message)
                return False

        send = t.await_selections_message

        try:
            await self.client.edit_message(confirmation, send)
        except:
            # If confirmation is turned off, a new message will need to be
            #    sent instead of editing the old one
            await self.client.send_message(msg.channel, send)

        # Return question string
        return new_question

    async def _prompt_selections(self, msg):
        channel = msg.channel
        selection_limit = 10

        selections = []

        # Repeat for up to 10 selection options
        for i in range(selection_limit):
            response = await self.client.wait_for_message(
                timeout = config.submit_selection_timeout,
                channel = msg.channel,
                author = msg.author
            )

            # If response is invalid for some reason
            if not response.type == MessageType.default and len(response.content) > 0:
                await self.client.send_typing(channel)
                await self.client.send_message(create_poll_cancelled_message)
                return False

            if response == None:
                # If no message was sent before timeout ended, abort
                await self.client.send_typing(channel)
                await self.client.send_message(channel, t.add_selection_cancelled_message)
                return False
            elif response.content.lower() == "stop":
                # If user sent 'stop', exit
                await self.client.send_typing(channel)
                await self.client.send_message(channel, t.create_poll_cancelled_message)
                return False
            elif response.content.lower() == "done":
                if i == 0:
                    # If they said 'done' without entering any options, exit
                    await self.client.send_typing(channel)
                    await self.client.send_message(channel, t.create_poll_cancelled_message)
                    return False
                else:
                    break

            selections.append(response.content)

        # Return selections array
        return selections

    async def _confirm_poll(self, msg, poll):
        channel = msg.channel

        preview_embed = poll.get_preview_embed()

        if preview_embed == False:
            await self.client.send_typing(channel)
            await self.client.send_message(channel, t.try_again_message)
            return False

        # Verify with user this poll is all correct
        repost = await self.client.send_message(channel, embed=preview_embed)
        await self.client.send_typing(channel)
        confirmation = await self.client.send_message(channel, t.confirm_poll_preview_message)

        # Create confirm reactions
        await self.client.add_reaction(confirmation, t.yes_emoji)
        await self.client.add_reaction(confirmation, t.no_emoji)

        # Wait for user to select one
        res = await self.client.wait_for_reaction(
            message = confirmation,
            emoji = [t.yes_emoji, t.no_emoji],
            user = msg.author,
            timeout = config.confirm_reaction_timeout
        )

        if res == None:
            await self.client.delete_message(repost)
            await self.client.clear_reactions(confirmation)
            await self.client.edit_message(confirmation, t.confirm_reaction_timeout_message)
            return False

        if res.reaction.emoji == t.yes_emoji:
            await self.client.delete_message(repost)
            await self.client.clear_reactions(confirmation)
        elif res.reaction.emoji == t.no_emoji:
            await self.client.delete_message(repost)
            await self.client.clear_reactions(confirmation)
            await self.client.edit_message(confirmation, t.create_poll_cancelled_message)
            return False
        else:
            await self.client.send_typing(channel)
            await self.client.send_message(channel, t.try_again_message)
            return False

        await self.client.edit_message(confirmation, t.poll_created_message)
        return True

    async def _create_poll_message(self, msg, poll):
        channels = msg.server.channels
        server_model = database.get_or_make_server_model(msg.server)

        poll_channel = None

        # If the server has a poll channel saved, retrieve it, and make sure
        #    it is both valid, and we have permission to send messages in it
        if server_model.poll_channel_id != None:
            c = msg.server.get_channel(server_model.poll_channel_id)
            if c != None:
                if c.permissions_for(msg.server.me).send_messages:
                    poll_channel = c

        # If there wasn't a saved poll channel that could be used, select a
        #    channel arbitrarily
        if poll_channel == None:
            for c in channels:
                if c.type == ChannelType.text:
                    if c.permissions_for(msg.server.me).send_messages:
                        poll_channel = c
                        break

        if poll_channel == None:
            # Break if the poll channel somehow couldn't be resolved
            return False

        # Create the actual poll post
        try:
            poll_message = await self.client.send_message(poll_channel, embed=poll.get_embed())
        except:
            # Request failed, probably due to embed content being too long
            await self.client.send_message(msg.channel, t.poll_too_long_message)
            return False

        # Add the reactions (poll options) to the post
        for sel in poll.selections:
            await self.client.add_reaction(poll_message, sel.emoji)

        return poll_message

    async def _show_poll_results(self, msg, poll):
        channels = msg.server.channels
        server_model = database.get_or_make_server_model(msg.server)

        poll_channel = None

        # If the server has a poll channel saved, retrieve it, and make sure
        #    it is both valid, and we have permission to send messages in it
        if server_model.poll_channel_id != None:
            c = msg.server.get_channel(server_model.poll_channel_id)
            if c != None:
                if c.permissions_for(msg.server.me).send_messages:
                    poll_channel = c

        # If there wasn't a saved poll channel that could be used, select a
        #    channel arbitrarily
        if poll_channel == None:
            for c in channels:
                if c.type == ChannelType.text:
                    if c.permissions_for(msg.server.me).send_messages:
                        poll_channel = c
                        break

        if poll_channel == None:
            # Break if the poll channel somehow couldn't be resolved
            return False

        # Send poll results to channel!

        try:
            await self.client.send_message(poll_channel, embed=poll.get_results_embed())
        except:
            # Embed content may have been too long - try sending shortened version
            try:
                await self.client.send_message(poll_channel, embed=poll.get_embed(short_embed=True))
            except:
                # If that didn't work just break
                return

    async def execute(self, msg, args):

        question = await self._prompt_question(msg)
        if question == False:
            return

        selections = await self._prompt_selections(msg)
        if selections == False:
            return

        poll = Poll(question, selections, msg.author)

        if config.show_poll_preview:
            # Confirm poll with user
            # (If they approve, 'poll created' message will be sent as part of this function)
            if not await self._confirm_poll(msg, poll):
                return
        # Otherwise, just announce poll creation
        else:
            await self.client.send_message(msg.channel, t.poll_created_message)

        poll_message = await self._create_poll_message(msg, poll)
        if poll_message == False:
            return

        active_polls.append({
            'poll': poll,
            'message': poll_message
        })

        await sleep(config.poll_duration*60)

        w = poll.make_winners()

        await self.client.edit_message(poll_message, embed=poll.get_embed(is_active=False))
        await self.client.clear_reactions(poll_message)

        if w == False:
            return # Nobody voted, pack it up boys

        await self._show_poll_results(msg, poll)
