import functools

def cache_result(func):
    '''Methods with this decorator will use controller's CACHE when possible:
    '''
    func.cache_result = True
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapped
