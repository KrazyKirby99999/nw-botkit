import os
import json
import hashlib
from .decorators import cache_result

class NoCache:
    def get_result(self, room, event):
        return None

    def set_result(self, content, room, event):
        pass

class InMemoryTextCache:
    cache = {}

    def get_result(self, room, event):
        txt = event.body.strip()
        return self.cache.get(txt)

    def set_result(self, content, room, event):
        txt = event.body.strip()
        self.cache[txt] = content

class FileTextCache:

    def __init__(self, cache_dir=None):
        if not cache_dir:
            cache_dir= os.getcwd()
        self.cache_dir = cache_dir

    def get_result(self, room, event):
        txt = event.body.strip()
        txt_hash = self._get_file_name(txt)
        file_path = os.path.join(self.cache_dir, txt_hash)
        if os.path.isfile(file_path):
            with open(file_path,'r') as f:
                return json.load(f)
        return None

    def set_result(self, content, room, event):
        txt = event.body.strip()
        txt_hash = self._get_file_name(txt)
        file_path = os.path.join(self.cache_dir, txt_hash)
        with open(file_path, 'w') as f:
            json.dump(content, f)

    def _get_file_name(self, txt):
        txt_encoded = txt.encode('utf-8')
        m = hashlib.sha256()
        m.update(txt_encoded)
        return f'{m.hexdigest()}.json'
