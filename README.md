# nw-botkit

nw-botkit is a library for quickly building Matrix bots. It uses [matrix-nio](https://github.com/poljar/matrix-nio) as its Matrix client library. This project is a fork of noteworthy-botkit that intends to continue improving.

## Examples

### XKCD Bot

```python
import os
import pathlib
import requests
from lxml import html

import nw.botkit as botkit
import nw.botkit.response as response
import nw.botkit.cache as cache

XKCD_PATH = pathlib.Path(__file__).parent.absolute()
CACHE_PATH = os.path.join(XKCD_PATH, 'responsecache')


@botkit.botkit_controller(bot_name='xkcdbot')
class XKCDBotController():

    AUTH = botkit.auth.PublicBot
    CACHE = cache.FileTextCache(CACHE_PATH)

    @cache.cache_result
    @botkit.botkit_method
    async def num(self, num, **kwargs):
        page_url = f'https://xkcd.com/{num}/'
        img_url = self._get_img_url(page_url)
        return response.Image(img_url)

    def _get_img_url(self, url):
        res = requests.get(url)
        tree = html.fromstring(res.text)
        img_url = tree.xpath('//div[@id="comic"]/img')[0].get('src')
        return f'https:{img_url}'

creds = {
    'homeserver': 'https://matrix.MYSERVER.com',
    'user': '@bot:MYSERVER.com',
    'password': 'bot_password'
}

bot = XKCDBotController.create_matrix_bot(creds)
bot.run()
```

Accepts all invites and responds to all users. Fetches XKCD image with:

        !xkcdbot num <xkcd_comic_number>

Images are cached in local folder.

### Dice Bot

```python
import random
import re

import nw.botkit as botkit
import nw.botkit.response as response
import nw.botkit.cache as cache

@botkit.botkit_controller(bot_name='dicebot', bot_prefix='!dice')
class DiceBotController():

    AUTH = botkit.auth.PublicBot

    @botkit.botkit_method
    async def roll(self, dstring, **kwargs):
        regex = re.compile('^([0-9]+)d([0-9]+)$')
        match = re.search(regex, dstring)
        num_dice = int(match.group(1))
        sides = int(match.group(2))
        res = []
        for d in range(num_dice):
            res.append(random.randint(1,sides))
        return response.Notice(f'rolling {dstring}: {res}')

creds = {
    'homeserver': 'https://matrix.MYSERVER.com',
    'user': '@bot:MYSERVER.com',
    'password': 'bot_password'
}

bot = DiceBotController.create_matrix_bot(creds)
bot.run()
```

Accepts all invites and responds to all users. Produces dice rolls in `<N>d<S>` format with:

    !dice roll <number_of_dice>d<number_of_sides>

## Decorators

### botkit_controller

Requires specifying a `bot_name` - bots are invoked by writing `<bot_prefix> <method>` in chat. The `bot_prefix` is `!<bot_name>` by default, but can be specified otherwise. Marks a python class as a bot controller. Adds `create_matrix_bot` class method that takes in `creds` and creates a bot. The bot's `run` starts the bot and blocks while the bot is running.

#### creds

`creds` is a dictionary with `homeserver`, `user`, and `password` credentials for a bot.

### botkit_method

Marks a function as a bot method. Can be invoked with `<bot_prefix> <function_name>`

#### cache_result

A `botkit_method` marked with this will have its result cached. If the exact invocation of the command has been called before, bot will return the result without calling the function again.

### botkit_msg_handler

A function marked with this will be invoked upon processing all non-command messages

### botkit_startup_method

A function marked with this will execute one time when the bot's `run` is invoked.

## Auth

A matrix bot controller can specify it's invite acceptance and command invocation authorization by setting `AUTH`.

### BlockAll

This is the default if `AUTH` is not specified. Will not accept any invites and will not respond to any commands.

### PublicBot

The bot will accept all invites and respond to all commands.

### UserWhitelist

The bot will only accept invites from and respond to commands from users specified in `USER_WHITELIST` list on the controller class.

## Response

### Text

TODO

### Notice

TODO

### Html

TODO

### Image

TODO

## Cache

### NoCache

Default. No cacheing.

### InMemoryTextCache

Stores cached command results in memory.

### FileTextCache

Stores cached command results on disk.
