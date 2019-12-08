import asyncio
import itertools
from urllib.parse import urlencode
from aiohttp import hdrs, ClientSession

class CloudPiercerException(Exception):
    pass

class CloudPiercer:

    def __init__(self, solver_endpoint):
        self.solver_endpoint = solver_endpoint

    async def solve(self, url, html):
        solver_url = self.solver_endpoint + '?' + urlencode({'url': url})
        async with ClientSession() as sess:
            async with sess.post(solver_url, data=html) as resp:
                obj = await resp.json()
                return obj['url'], obj['data']

    async def fetch(self, sess, url, extra_headers={}, with_text=False):

        # Cloudflare seems to do a bit of browser fingerprinting. This combination of headers works at time of writing.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            }

        headers.update(extra_headers)

        method = hdrs.METH_GET
        data = None

        for i in itertools.count(0):
            async with sess.request(method, url, headers=headers, data=data, allow_redirects=False) as resp:
                if resp.status == 403:
                    raise CloudPiercerException('captcha')
                elif resp.status == 503:
                    if i > 5:
                        raise CloudPiercerException('loop')
                    else:
                        text = await resp.text()
                        url, data = await self.solve(resp.url, text)
                        method = hdrs.METH_POST
                        await asyncio.sleep(6)
                else:
                    if with_text:
                        text = await resp.text()
                    else:
                        text = None
                    return resp, text
