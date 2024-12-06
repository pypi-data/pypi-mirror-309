import aiohttp
import asyncio

from src.igloohome_api import Api
from src.igloohome_api import Auth


async def run():
    trace = aiohttp.TraceConfig()
    session = aiohttp.ClientSession(trace_configs=[trace])
    try:
        auth = Auth(
            client_id="74s4953upvhp8o7kenvul8qick",
            client_secret="hoouddc2ackch07h9juq3f1kn2kpjvql5ic2jrdjhmi7tmnfr6u",
            session=session,
        )
        api = Api(auth=auth)
        print(f'response={(await api.get_devices()).payload[0].deviceId}')
    finally:
        await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
