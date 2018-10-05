> **Language:** Python 3

> **Libraries:** [discord.py](https://github.com/Rapptz/discord.py) \| [peewee](http://docs.peewee-orm.com/en/latest/) \| [ccxt](odajsd) \| [requests](ajsdoi)

> **Database:** MySQL

> **Author:** [Sparrowing on GitHub](https://github.com/sparrowing) \| [sparrowing on Fiverr](https://www.fiverr.com/sparrowing)

# Config

All configuration settings are read from a file named `config.py`.  File MUST have this exact name or it will not be recognized.  A sample configuration file containing default or placeholder values is included, but is incomplete and will not work on its own (instructions in Installation).  They follow a key/value structure declared with an equals sign, i.e. `key = value`.  'Key' names must not be edited or they will not be recognized, and should thus not be touched.  Values written within `"quotes"` should stay in quotes, and those that are not should also remain that way.

**All included config values:**
* `token` - The bot user token.  Allows the client to connect to Discord.
* `prefix` - The prefix that will be used in front of bot commands.  Tells the bot what messages to pay attention to.
* `bot_username` - Displayed username of the bot user (may still be overridden by individual nicknames in servers).  If this value is edited, the bot name will automatically be updated next time the bot is started.
* `playing_message` - The 'game playing' message that will display for the bot, e.g. "Playing **Game**".  If this value is edited, the playing status will automatically be updated next time the bot is started.
* `db_host` - Host address of the database to connect to.
* `db_port` - Port number of the database to connect to.  Should not have quotes around it.
* `mysql_db_name` - Name of the database that is being connected to.
* `mysql_db_username` - User to connect to the database with.  Typically the same as `mysql_db_name` depending on database setup.
* `mysql_db_password` - Password of the user to connect to the database with.
* `cryptopia_api_key` - API key for Cryptopia.  Ticker functions won't work properly without this.  Can easily be generated on Cryptopia's website.
* `embed_color` - The color that displays on the side of embeds created by this bot.  Must match a specific number format.  These can be easily generated on sites such as [leovoel's embed visualizer](https://leovoel.github.io/embed-visualizer/).
* `confirm_database_submissions` - If set to `True`, when submitting meme submissions of any kind, the bot will allow you to confirm your submission is correct before submitting it.  Set this to `False` to have it just submit them immediately.
* `confirm_poll_creation` - If set to `True`, when creating a new poll, the bot will allow you to confirm your question is correct before proceeding.  Set this to `False` to have it jump straight to specifying poll options.
* `show_poll_preview` - If set to `True`, after specifying all fields for a new poll, the bot will generate a preview of what the poll embed will look like and allow you to confirm it looks correct before opening the poll.  Set this to `False` to have the poll be immediately opened and sent to the poll channel.
* `poll_duration` - The length, **in minutes**, that polls should run before closing.  (Decimal values are allowed.)
* `add_row_timeout` - When submitting a new database submission, this is the amount of time (**in seconds**) that the bot will wait for a submission after calling the !add command.
* `confirm_reaction_timeout` - For any instance where the bot is waiting for a yes/no confirmation reaction, this is how long the bot will wait (**in seconds**) for the user to select a response before timing out.
* `create_question_timeout` - When creating a new poll, this is the amount of time (**in seconds**) that the bot will wait for your question after calling the !poll command.
* `submit_selection_timeout` - When listing selection options for a new poll, this is the amount of time (**in seconds**) that the bot will wait for a selection option before timing out.  This timeout refreshes each time a new selection is listed.
* `withdrawals_list_limit` - When using the !withdrawals command, this is how many transaction IDs the bot will list at maximum.  Note that making this value too large may risk the bot's message hitting Discord's character limit and failing to display.
* `deposits_list_limit` - When using the !deposits command, this is how many transaction IDs the bot will list at maximum.  Note that making this value too large may risk the bot's message hitting Discord's character limit and failing to display.
* `tip_list_limit` - When using the !tips command, this is how many tip records the bot will list at maximum.  Note that this applies for BOTH given and received tips - if this value is set to 5, then 5 given tips will display, AND 5 received tips.  Be very careful as making this value too large may risk the bot's message hitting Discord's character limit and failing to display.
* `bet_payout_dubs` - When using the !bet command, this is the payout multiplier that will be applied when winning dubs.
* `bet_payout_trips` - When using the !bet command, this is the payout multiplier that will be applied when winning trips.
* `bet_payout_quads` - When using the !bet command, this is the payout multiplier that will be applied when winning quads.

# Commands

**Basic Commands:**
Command Name | Usage | Requirements | Description
`commands` | `!commands` | None | joaisd
`help` | `!help <command_name>` or `!help` | `!help` must have DMs enabled | ajosdijf
`ping` | `!ping` | None | Ping pong!
`setwelcomechannel` | `!setwelcomechannel` | Requires admin privileges on bot / must be in a text channel of a server that bot has permissions to speak in | sjdoaisd
`setpollchannel` | `!setpollchannel` | Requires admin privileges on bot / must be in a text channel of a server that bot has permissions to speak in | asdjofj

**Persistence Commands:**

**Meme Commands:**

**Poll Commands:**

**Ticker Commands:**

**Transaction Commands:**

**Other Commands:**

# Installation

These installation instructions are by no means complete.  Parts of installation and deployment such as installing dependencies, running MySQL, hosting, and uploading to a server are the responsibility of the person running the bot.

**Prerequisites:**
* Must have a recent version of Python 3 installed.
* Must have all necessary Python dependencies installed.  (All required dependencies are listed within the `requirements.txt` file.)

---

1. **Set up bot user**

    Create an application inside Discord's [developer portal](https://discordapp.com/developers/applications/).  Go to the 'bot' section and select create a bot user.  This page is also where you can set your bot's avatar.

2. **Find bot token**

    Find the 'token' section where there should be something that says 'click to reveal token'.  Copy this token to your clipboard.

3. **Enter sample_config.py**

    In the files of this bot, open `sample_config.py` in a plain text editor.  Notepad will work fine.  Do NOT use Microsoft Word or other document-editing programs.

4. **Insert bot token**

    Go to 'token' value at the top of this file.  Inside of the quotes, replace `your_token` with the token you added from the developer portal.

5. **Prepare MySQL**

    Be sure you have a running instance of MySQL and an empty database for the bot.  The bot will automatically create the needed database tables.  Note: If MySQL is not running, or the bot does not have the permissions for the database, the bot will NOT RUN.  If the bot is failing, make sure MySQL is running and configured properly.

6. **Finish config**

    Replace `cryptopia_api_key` with your API key.  Replace `db_host`, `db_port`, `mysql_db_name`, `mysql_db_username`, `mysql_db_password` with your own settings.  Tweak any other config values however you need.  `mysql_db_name` will be the name of the database created for the previous step.

7. **Rename sample_config.py to config.py**

    Rename the file to the exact name `config.py` so that the bot will recognize it as the config file it needs to be reading.

7. **Run bot**

    Using Python, run the file `bot.py`, and you're good to go!
