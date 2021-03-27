import random
import re

import nw.botkit as botkit
import nw.botkit.response as response
import nw.botkit.cache as cache

@botkit.botkit_controller(bot_name='echobot', bot_prefix='!bot')
class EchoBotController():

    AUTH = botkit.auth.PublicBot

    @botkit.botkit_method
    async def echo(self, dstring, **kwargs):
        message = str(dstring)
        for kw in kwargs:
          message = message + str(kw)
        return response.Notice(message[:-7])

creds = {
    'homeserver': 'https://matrix.MYSERVER.com',
    'user': '@bot:MYSERVER.com',
    'password': 'bot_password'
}

bot = EchoBotController.create_matrix_bot(creds)
bot.run()
