# Bible Bot

Provides links to different translations of a random verse from the bible.
Can post on Mastodon and Signal.

## Run

1. Clone the project with Git or download it as a ZIP.
2. Copy the file `config-template.ini` to `config.ini` and edit the copy so that the data
   in it is correct. Also see below for explanations of the settings.
3. Python 3.9 or higher and the necessary libraries must be installed 
   (e.g. with the command `pip3 install -r requirements.txt`). Recommendation: Use a 
   [venv](https://docs.python.org/3/library/venv.html) and install the libraries in it.
4. Run either `bot_console.py`, `bot_mastodon.py` or `bot_signal.py` periodically, e.g. once a day.

### Console

Simply outputs the message as text. Useful for shell scripts.

### Mastodon

Posts the message as a status in Mastodon. The Mastodon account used must be
configured with the following settings:

- `api_base_url`: the address of the Mastodon instance
- `access_token`: the access token of the Mastodon "application" (see below)

In the Mastodon settings there is the "Development" section and there the
"New Application" button. There must be an application that has at least the permission
`write:statuses` - the token from this must be configured in the bot.

### Signal

Posts the message as a Signal message in as many direct chats and/or groups as you like. 
Access to signal-cli is via DBus. Required settings for the bot:

- `sender`: the number that should send the messages (must be configured in signal-cli)
  in the format 49123456789
- `recipients` (optional): `|`-separated list of numbers in the format +49123456789,
  to which the messages should be sent directly
- `groups` (optional): `|`-separated list of group names of which `sender` is a member -
  the message will be posted in these groups

## Global settings

- `translations`: used to generate the links to the bible verse, example:  
  `NIV=New International Version|ELB=Elberfelder Bibel`
- `language`: use book names and abbreviations in this language - the file
  `books_XY.csv` has to exist in subdirectory `data` if language is set to XY