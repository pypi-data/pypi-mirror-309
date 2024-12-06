import json
import urllib.request


class XimalayaClient:
    def __init__(self, host: str = 'www.ximalaya.com', headers: dict = None):
        self.host = host
        self.headers = ({} if headers is None else headers) | {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

    def request(self, path: str, method: str = 'GET'):
        url = f'https://{self.host}/{path.lstrip("/")}'

        req = urllib.request.Request(url, headers=self.headers, method=method)
        with urllib.request.urlopen(req) as f:
            return json.loads(f.read().decode('utf-8'))
