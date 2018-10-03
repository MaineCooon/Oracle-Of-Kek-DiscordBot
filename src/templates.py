import config

yes_emoji = '👍'
no_emoji = '👎'

welcome_message = "Welcome {username_tag}!  Praise KeK!"

donate_message = "If you would like to support KekCoin you can contribute to " \
        "the following addresses:\n\nBTC:\nKEK:"

poll_description = "React with the number that corresponds to your response! " \
        "The poll will close after {poll_duration} minutes. (Note: Voting multiple times will " \
        "only count the most recent response.)" \
        .format(poll_duration=config.poll_duration)

admin_added_message = "{username_tag} added as an admin!"

display_supply_message = "{supply} KEK"
supply_unavailable_message = "Sorry!  Unable to retrieve supply information."

display_price_message = \
        "**Cryptopia: {btc_price} BTC | ${usd_price}**\n" \
        "Vol: {volume} KEK\n" \
        "Low: {low_24h} | High: {high_24h}\n" \
        "24h Change: {change_24h}%"
price_unavailable_message = "Sorry!  Unable to retrieve price information."

display_blockchain_message = \
        "Block Count: {block_count}\n" \
        "Staking Weight: {staking_weight}\n" \
        "Staking Reward: {staking_reward}\n" \
        "Difficulty: {difficulty}\n" \
        "Blockchain Size: {blockchain_size}"
blockchain_unavailable_message = "Sorry!  Unable to retrieve blockchain information."

display_mcap_message = \
        "${mcap_usd} | {mcap_btc} BTC\n" \
        "Position: {position}"
mcap_unavailable_message = "Sorry!  Unable to retrieve mcap information."

add_cancelled_message = "Took longer than {timeout} seconds, cancelled." \
        .format(timeout=config.add_row_timeout)
add_stopped_message = "!add stopped."
await_submission_message = "Please send submission.  (Or 'stop' to exit.)"
invalid_submission_message = "Sorry, what you sent is not valid for the submission type."
confirm_submission_message = "Is this submission correct?  React {yes_emoji} to " \
        "confirm, {no_emoji} to cancel." \
        .format(yes_emoji=yes_emoji, no_emoji=no_emoji)
confirm_reaction_timeout_message = "No response in {reaction_timeout} seconds, cancelled." \
        .format(reaction_timeout=config.confirm_reaction_timeout)

submission_cancelled_message = "Database submission cancelled."
pending_submission_message = "Submitting..."
submission_complete_message = "Submission added!"
submission_failed_message = "Submission failed.  Please try again."

create_question_cancelled_message = "Took longer than {timeout} seconds, cancelled." \
        .format(timeout=config.create_question_timeout)
create_question_stopped_message = "!poll stopped."
await_question_message = "Thanks for creating a poll!  Please enter the question " \
        "you would like to poll for.  (Or 'stop' to exit.)"
invalid_question_message = "Invalid submission, poll creation cancelled."
confirm_question_message = "Is this question correct?  React {yes_emoji} to confirm, " \
        "{no_emoji} to cancel." \
        .format(yes_emoji=yes_emoji, no_emoji=no_emoji)
create_poll_cancelled_message = "Poll creation cancelled."

await_selections_message = "Great!  Begin listing your poll options, one message per each selection (limit 10).  " \
        "Say 'done' to finish adding selections, or 'stop' to cancel poll creation."
add_selection_cancelled_message = "Poll creation cancelled, no response in {timeout} seconds." \
        .format(timeout=config.submit_selection_timeout)

confirm_poll_preview_message = "Does this poll look good?  React {yes_emoji} to confirm, " \
        "{no_emoji} to cancel poll creation." \
        .format(yes_emoji=yes_emoji, no_emoji=no_emoji)
poll_preview_description = "This is just a preview for the poll creator to confirm " \
        "the contents of this poll.  'Voting' on this won't do anything."
poll_too_long_message = "Poll creation failed, poll content was likely too long.  Poll creation cancelled."
poll_created_message = "Poll has been created!"

no_keks_saved_message = "Sorry!  There are currently no kek quotes in our database."
no_trumps_saved_message = "Sorry!  There are currently no Trump quotes in our database."
no_memes_saved_message = "Sorry!  There are currently no meme images in our database."
no_gifs_saved_message = "Sorry!  There are currently no gifs saved in our database."
no_advice_saved_message = "Sorry!  There is currently no advice saved in our database."

content_not_loaded_message = "Sorry, the content failed to display for some reason.  Try again!"

try_again_message = "Sorry!  Something went wrong.  Please try again."

poll_footer_text = "Poll created by {username}"
poll_closed_description = "Poll has been closed.  No more voting will be counted."

number_emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
