import os

import aiohttp

from app.internal.schemas.currency import Symbols
from app.pkg.redis_tools.tools import RedisTools


async def on_startup():
    async with aiohttp.ClientSession() as session:
        async with session.get(os.environ.get("ALL_PAIRS_KEY")) as response:
            response_json = await response.json()

            parsed_pairs = Symbols(**response_json)

            cutted_pairs = parsed_pairs.symbols[:20]

            symbols = [pair.symbol for pair in cutted_pairs]

            for symbol in symbols:
                RedisTools.set_pair(symbol, 0)


async def on_loop_startup():
    for symbol in RedisTools.get_keys():
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{os.environ.get("CURRENCY_PAIR_KEY")}{symbol.decode("utf-8")}') as response:
                responce_json = await response.json()
                RedisTools.set_pair(symbol, responce_json['price'])
