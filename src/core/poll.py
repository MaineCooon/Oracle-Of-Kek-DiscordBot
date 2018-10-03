from discord import Embed

import config
import templates

class PollSelection():
    def __init__(self, str, number):
        self.str = str
        self.number = number
        self.voters = []
        self.emoji = templates.number_emojis[number]
        self.is_winner = False

    @property
    def votes(self):
        return len(self.voters)

class Poll():
    def __init__(self, question, selections, created_by):
        self.question = question
        self.selections = self._create_selection_objects(selections)
        self.created_by = created_by
        self.duration = config.poll_duration

    def _create_selection_objects(self, selection_strings):
        arr = []
        for i in range(len(selection_strings)):
            s = PollSelection(selection_strings[i], i)
            arr.append(s)
        return arr

    def _get_options_string(self):
        number_emojis = templates.number_emojis
        str = ''
        for i in range(len(self.selections)):
            if i != 0:
                str += "\n\n"
            str += "{} {}".format(number_emojis[i], self.selections[i].str)
        return str

    def get_total_votes(self):
        count = 0
        for sel in self.selections:
            count += sel.votes
        return count

    def get_winning_selections(self):
        top_votes = 0
        winners = []
        for sel in self.selections:
            if sel.votes > top_votes:
                top_votes = sel.votes
                winners.clear()
                winners.append(sel) # Set the new winner
            elif sel.votes == top_votes:
                # If two winners tie, have them both in an array
                winners.append(sel)
        if top_votes > 0:
            return winners
        else:
            return False

    def make_winners(self):
        winners = self.get_winning_selections()
        if winners == False:
            return False
        for w in winners:
            w.is_winner = True

    def add_vote(self, user, number):
        # Remove any other vote(s) by this user
        for sel in self.selections:
            if user.id in sel.voters:
                sel.voters.remove(user.id)

        # Add the voter to the chosen selection's list of voters
        (self.selections[number].voters).append(user.id)

    def get_emoji_array(self):
        arr = []
        for sel in self.selections:
            arr.append(sel.emoji)
        return arr

    def get_preview_embed(self):
        embed = False
        try:
            embed = Embed(
                title = self.question,
                description = templates.poll_preview_description,
                color = config.embed_color
            ).add_field(
                name = "Options",
                value = self._get_options_string()
            ).set_footer(
                text = templates.poll_footer_text.format(
                    username = self.created_by.nick if (self.created_by.nick != None) else self.created_by.name
                )
            )
        except:
            return False
        return embed

    def get_results_embed(self, short_embed=False):
        embed = False
        try:

            # Make winner announcement string

            winners = self.get_winning_selections()
            if not winners:
                return False
            if len(winners) > 1:
                description = "And the winners are: **{}** !".format(
                    "** and **".join([w.str for w in winners])
                )
            else:
                description = "And the winner is: **{}** !".format(
                    winners[0].str
                )

            # Create embed

            embed = Embed(
                title = self.question,
                description = description,
                color = config.embed_color
            ).set_footer(
                text = templates.poll_footer_text.format(
                    username = self.created_by.nick if (self.created_by.nick != None) else self.created_by.name
                )
            )

            if not short_embed:
                # Add individual selection stats to embed

                total_votes = self.get_total_votes()

                for sel in self.selections:
                    name = "{} {}".format(sel.emoji, sel.str)

                    vote_count = sel.votes
                    word_tense = "vote" if vote_count == 1 else "votes"
                    percentage = round( (vote_count / total_votes) * 100, 1)
                    percent_string = "{:.1f}".format(percentage).rstrip('0').rstrip('.')

                    if sel.is_winner:
                        value = "**{} {} | {}% of the vote**".format(str(vote_count), word_tense, percent_string)
                    else:
                        value = "{} {} | {}% of the vote".format(str(vote_count), word_tense, percent_string)

                    embed.add_field(name=name, value=value, inline=False)
        except:
            return False
        return embed

    def get_embed(self, is_active=True):
        embed = False
        try:
            embed = Embed(
                title = self.question,
                description = templates.poll_description if is_active else templates.poll_closed_description,
                color = config.embed_color
            ).add_field(
                name = "Options",
                value = self._get_options_string()
            ).set_footer(
                text = templates.poll_footer_text.format(
                    username = self.created_by.nick if (self.created_by.nick != None) else self.created_by.name
                )
            )
        except:
            return False
        return embed
