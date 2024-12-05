import asyncio
from xync_client.Abc.Agent import AgentClient


async def test_payment_methods():
    result = await AgentClient.payment_methods()
    return result


asyncio.run(test_payment_methods())
