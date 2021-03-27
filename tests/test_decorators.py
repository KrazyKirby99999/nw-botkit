from nw import botkit

class TestDecorators:

    def test_botkit_method_(self):
        @botkit.botkit_method
        def fake():
            pass
        assert fake.botkit_method

    def test_botkit_msg_handler(self):
        @botkit.botkit_msg_handler
        def fake():
            pass
        assert fake.botkit_msg_handler

    def test_botkit_startup_method(self):
        @botkit.botkit_startup_method
        def fake():
            pass
        assert fake.botkit_startup_method

    def test_botkit_controller(self):
        bot_name = 'fakebot'
        greeting = 'fake greeting!'

        @botkit.botkit_controller(bot_name, channel_greeting = greeting)
        class Fake:
            pass
        pass

        assert Fake.botkit_controller
        assert Fake.BOTKIT_BOT_NAME == bot_name
        assert Fake.CHANNEL_GREETING == greeting

        assert Fake.create_matrix_bot
        fake_creds = {
            'homeserver': 'fake.im',
            'user': '@fake:fake.im',
            'password': 'fake'
        }
        bot = Fake.create_matrix_bot(fake_creds)
        assert bot
