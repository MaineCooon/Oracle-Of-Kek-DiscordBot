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

tipping_account_exists_message = "Tipping account already exists for user {username_tag}.  " \
        "Try {prefix}deposit to check deposit address."
no_tipping_account_exists_message = "No tipping account registered for {username_tag}.  Please " \
        "create one using {prefix}register to do this."
tipping_account_creation_failed_message = "Creation of tipping account failed.  Please try again."
tipping_account_created_message = "Your tipping account has been generated for {username_tag}."
balance_unavailable_message = "Unable to retrieve balance for {username_tag}."
invalid_address_message = "Invalid deposit address."
cant_withdraw_amount_message = "Unable to withdraw this amount.  You may not have enough in " \
        "your KekBot account.  Use {prefix}balance to check your current balance." \
        .format(prefix=config.prefix)
withdrawal_failed_message = "Withdrawal failed.  Please try again."
withdrawal_completed_message = "Withdrawal complete!"

tip_failed_message = "Tip failed.  Please try again."
tip_completed_message = "Tip completed!"

display_balance_message = "{balance} KEK"

withdrawal_history_message = "**Withdrawal History:**\n{withdrawals}"
deposit_history_message = "**Deposit History:**\n{deposits}"

list_withdrawals_failed_message = "Withdrawal list failed.  Please try again."
list_deposits_failed_message = "Deposit list failed.  Please try again."
list_tips_failed_message = "Tip list failed.  Please try again."

list_sent_tips = "Sent to: {username_tag} | Amount: {amount} KEK"
list_received_tips = "Received from: {username_tag} | Amount: {amount} KEK"

poll_footer_text = "Poll created by {username}"
poll_closed_description = "Poll has been closed.  No more voting will be counted."

cant_bet_amount_message = "Unable to bet this amount.  You may not have enough in " \
    "your KekBot account.  Use {prefix}balance to check your current balance." \
    .format(prefix=config.prefix)
announce_dubs_message = "{number} DUBS!\nYou have won {payout} KEKs"
announce_trips_message = "{number} TRIPS!\nYou have won {payout} KEKs"
announce_quads_message = "{number} QUADS!\nYou have won {payout} KEKs"
bet_failed_message = "Bet failed.  Please try again."

usage_message = "**Usage:** {usage}"

number_emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
