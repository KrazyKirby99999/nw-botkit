import functools
from .bot import Bot

def botkit_method(func):
    '''Methods with this decorator will be invocable as a bot command:
       !<bot_name> <method_name> <args>
    '''
    func.botkit_method = True
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapped

def botkit_msg_handler(func):
    '''A Method with this decorator will handle all message events received by the bot.
       A context object with room and client objects will be passed in.
       Bot creation will throw if more than one method is marked.
    '''
    func.botkit_msg_handler = True
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapped

def botkit_startup_method(func):
    '''The Method marked with this decorator will be run once the bot logs in.
       The async client will be passed in.
       Bot creation will throw if more than one method is marked.
    '''
    func.botkit_startup_method = True
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapped


def botkit_controller(bot_name, channel_greeting=None, bot_prefix=None):
    '''Marks a class to generate a matrix bot.
       Marked class will get a create_matrix_bot method that will create a Bot instance.
    '''

    def botkit_controller_wrapper(cls):
        cls.botkit_controller = True
        cls.BOTKIT_BOT_NAME = bot_name
        cls.CHANNEL_GREETING = channel_greeting
        cls.BOTKIT_BOT_PREFIX = bot_prefix

        @staticmethod
        def create_matrix_bot(creds):
            controller = cls()
            return Bot(controller, creds)
        cls.create_matrix_bot = create_matrix_bot
        return cls
    return botkit_controller_wrapper
