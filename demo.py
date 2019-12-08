import asyncio
from argparse import ArgumentParser
from aiohttp import ClientSession
from cloudpiercer import CloudPiercer

SOLVER_ENDPOINT = 'http://localhost:8081/solve'

def main():
    parser = ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()

    cloudpiercer = CloudPiercer(SOLVER_ENDPOINT)

    async def go():
        async with ClientSession() as sess:
            resp, text = await cloudpiercer.fetch(sess, args.url, with_text=True)
        print(resp)
        print(text)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())

if __name__ == '__main__':
    main()
