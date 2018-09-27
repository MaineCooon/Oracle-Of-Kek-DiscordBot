from config import add_row_timeout

await_kek_message = "Please send Kek quote to submit.  (Or 'stop' to exit.)"

display_supply_message = "{supply} KEK"
supply_unavailable_message = "Sorry!  Unable to retrieve supply information."

display_price_message = \
    "**Cryptopia: {btc_price} BTC | ${usd_price}**\n" \
    "Vol: {volume} KEK\n" \
    "Low: {low_24h} | High: {high_24h}\n" \
    "24h Change: {change_24h}%"
price_unavailable_message = "Sorry!  Unable to retrieve price information."

welcome_message = "Welcome {username_tag}!  Praise KeK!"

add_cancelled_message = "Took longer than {timeout} seconds, cancelled." \
        .format(timeout=add_row_timeout)
add_stopped_message = "!add stopped."
invalid_submission_message = "Sorry, what you sent is not valid for the submission type."
confirm_submission_message = "Is this submission correct?  React :thumbsup: to " \
    "confirm, :thumbsdown: to cancel."

submission_cancelled_message = "Database submission cancelled."
pending_submission_message = "Submitting..."
submission_complete_message = "Submission added!"
submission_failed_message = "Submission failed.  Please try again."

try_again_message = "Sorry!  Something went wrong.  Please try again."

yes_emoji = '👍'
no_emoji = '👎'
