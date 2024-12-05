from asyncio import run

from x_model import init_db
from xync_schema import models
from xync_schema.models import Coin, Cur, Pm, Ad, Ex, Curex

from xync_client.Abc import PublicClient as BasePublicClient


class PublicClient(BasePublicClient):
    async def curs(self) -> list[Cur]:
        curs = (await self._post("/v1/p2p/pub/currency/queryAllCoinAndFiat"))["data"]["fiatInfoRespList"]
        curs = [(await Cur.update_or_create(ticker=cur["fiatCode"]))[0] for cur in curs]
        curexs = [Curex(cur=c, ex=self.ex) for c in curs]
        await Curex.bulk_create(curexs, ignore_conflicts=True)
        return curs

    async def coins(self, cur: Cur = None) -> list[Coin]:
        coins = (await self._post("/v1/p2p/pub/currency/queryAllCoinAndFiat"))["data"]["coinInfoRespList"]
        coins = [(await Coin.update_or_create(ticker=c["coinCode"]))[0] for c in coins]
        [await c.exs.add(self.ex) for c in coins]
        return coins

    async def pms(self, cur: Cur = None) -> list[Pm]:
        curs = (await self._post("/v1/p2p/pub/currency/queryAllCoinAndFiat"))["data"]["fiatInfoRespList"]
        pmcurs = {cur["fiatCode"]: cur["paymethodInfo"] for cur in curs}
        pp = {}
        [[pp.update({p["paymethodId"]: p["paymethodName"]}) for p in ps] for ps in pmcurs.values()]
        return pp

    async def ads(self, coin: Coin, cur: Cur, is_sell: bool, pms: list[Pm] = None) -> list[Ad]:
        pass


async def main():
    _ = await init_db("postgres://artemiev:@/af_", models, True)
    bg = await Ex.get(name="BitGet")
    cl = PublicClient(bg)
    # await cl.curs()
    # await cl.coins()
    await cl.pms()


run(main())
