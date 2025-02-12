#!/usr/bin/env python3
""" The coroutine will loop 10 times """
import random
import asyncio
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """
    Each time asynchronously wait 1 second,
    then yield a random number between 0 and 10.
    """
    for i in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
