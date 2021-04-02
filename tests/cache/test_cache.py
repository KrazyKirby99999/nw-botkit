import nw.botkit.cache as cache

class FakeEvent:
    def __init__(self, txt):
        self.body = txt

class TestCaches:

    def test_NoCache(self):
        e = FakeEvent('request')
        sut = cache.NoCache()
        assert not sut.get_result(None, e)
        sut.set_result({'some': True}, None, e)
        assert not sut.get_result(None, e)

    def test_InMemoryTextCache(self):
        e = FakeEvent('request')
        sut = cache.InMemoryTextCache()
        assert not sut.get_result(None, e)
        sut.set_result({'some': True}, None, e)
        assert sut.get_result(None, e).get('some')
