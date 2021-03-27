import requests
import io
from PIL import Image as Img

class Response:
    async def get_content(self, **kwargs):
        return {'msgtype': self.mtype, 'body': self.msg}

class Text(Response):
    mtype = 'm.text'
    def __init__(self, msg):
        self.msg = msg

class Notice(Response):
    mtype = 'm.notice'
    def __init__(self, msg):
        self.msg = msg

class HTML(Response):
    def __init__(self, html):
        self.html = html

    async def get_content(self, **kwargs):
        return {
            'msgtype': 'm.text',
            'format': 'org.matrix.custom.html',
            'formatted_body': self.html,
            'body': self.html
        }

class Image(Response):
    def __init__(self, url):
        self.url = url

    async def get_content(self, client):
        filename = self.url.split("/")[-1]
        res = requests.get(self.url)
        if res.status_code == 200:
            headers = res.headers
            mimetype = headers.get('Content-Type')
            size = len(res.content)
            stream = io.BytesIO(res.content)
            img = Img.open(stream)
            w,h = img.size
            r = await client.upload(lambda x, y: res.content, mimetype, filename = filename)

        return {
            'msgtype': 'm.image',
            'url': r[0].content_uri,
            'body': filename,
            'info': {
                'mimetype': mimetype,
                'size': size,
                'h': img.height,
                'w': img.width
            }
        }
