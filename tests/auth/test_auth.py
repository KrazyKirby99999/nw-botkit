from nw.botkit.auth import PublicBot, BlockAll, UserWhitelist

class FakeController:
    def __init__(self, whitelist):
        self.USER_WHITELIST = whitelist

class FakeEvent:
    def __init__(self, sender):
        self.sender = sender

def get_fake_controller(wl = []):
    return FakeController(whitelist=wl)

def get_fake_event(sender = None):
    return FakeEvent(sender)

class TestPublicBot:

    def setup_method(self):
        c = get_fake_controller()
        self.sut = PublicBot(c)

    def test_accepts_all_invites(self):
        e = get_fake_event()
        assert self.sut.authenticate_invite(None, e)

    def test_accepts_all_messages(self):
        e = get_fake_event()
        assert self.sut.authenticate_message(None, e)

class TestBlockAll:

    def setup_method(self):
        c = get_fake_controller(wl=['user'])
        self.sut = BlockAll(c)

    def test_blocks_all_invites(self):
        e = get_fake_event(sender='user')
        assert not self.sut.authenticate_invite(None, e)

    def test_blocks_all_messages(self):
        e = get_fake_event(sender='user')
        assert not self.sut.authenticate_message(None, e)

class TestUserWhiteList:

    def setup_method(self):
        c = get_fake_controller(wl=['auth_user'])
        self.sut = UserWhitelist(c)

    def test_blocks_invite_no_auth_user(self):
        e = get_fake_event(sender='no_auth_user')
        assert not self.sut.authenticate_invite(None, e)

    def test_blocks_message_no_auth_user(self):
        e = get_fake_event(sender='no_auth_user')
        assert not self.sut.authenticate_message(None, e)

    def test_accepts_invite_auth_user(self):
        e = get_fake_event(sender='auth_user')
        assert self.sut.authenticate_invite(None, e)

    def test_accepts_message_auth_user(self):
        e = get_fake_event(sender='auth_user')
        assert self.sut.authenticate_message(None, e)

    def test_blocks_invite_no_whitelist_attr(self):
        sut = UserWhitelist(None)
        e = get_fake_event(sender='no_auth_user')
        assert not sut.authenticate_invite(None, e)

    def test_blocks_message_no_whitelist_attr(self):
        sut = UserWhitelist(None)
        e = get_fake_event(sender='no_auth_user')
        assert not sut.authenticate_message(None, e)
