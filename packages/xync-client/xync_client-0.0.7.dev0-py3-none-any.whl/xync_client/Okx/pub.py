from asyncio import run

from x_model import init_db
from xync_schema import models
from xync_schema.models import Coin, Cur, Pm, Ad, Ex, Curex

from xync_client.Abc import PublicClient as BasePublicClient


class PublicClient(BasePublicClient):
    async def curs(self) -> list[Cur]:
        curs = (await self._get("/v3/users/common/list/currencies"))["data"]
        curs = [(await Cur.update_or_create(ticker=cur["isoCode"]))[0] for cur in curs]
        curexs = [Curex(cur=c, ex=self.ex) for c in curs]
        await Curex.bulk_create(curexs, ignore_conflicts=True)
        return curs

    async def coins(self, cur: Cur = None) -> list[Coin]: ...

    async def pms(self, cur: Cur = None) -> list[Pm]:
        pmcurs = {
            cur.ticker: (await self._get("/v3/c2c/configs/receipt/templates", {"quoteCurrency": cur.ticker}))["data"]
            for cur in await self.curs()
        }
        pp = {}
        [[pp.update({p["paymentMethod"]: p["paymentMethodDescription"]}) for p in ps] for ps in pmcurs.values()]
        pp = {k: v for k, v in sorted(pp.items(), key=lambda x: x[0])}
        return pp

    async def ads(self, coin: Coin, cur: Cur, is_sell: bool, pms: list[Pm] = None) -> list[Ad]:
        pass


async def main():
    _ = await init_db("postgres://artemiev:@/af_", models, True)
    bg = await Ex.get(name="Okx")
    cl = PublicClient(bg)
    # await cl.curs()
    # await cl.coins()
    await cl.pms()


run(main())
