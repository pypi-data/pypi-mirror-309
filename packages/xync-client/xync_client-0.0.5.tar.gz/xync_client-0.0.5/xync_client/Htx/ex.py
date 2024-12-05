from asyncio import run

from x_model import init_db
from xync_schema import models
from xync_schema.models import Ex, Coin, Cur, Pm, Ad

from xync_client.Abc.Ex import ExClient


class Client(ExClient):
    # 20: Get all pms
    async def pms(self) -> dict[int, dict]:
        pms = (await self._coin_curs_pms())["payMethod"]
        pmsd = {
            pm["payMethodId"]: {
                "name": pm["name"],
                "type_": pm["template"],
                "logo": pm.get("bankImage", pm["bankImageWeb"]),
            }
            for pm in pms
        }
        return pmsd

    # 21: Get all: currency,pay,allCountry,coin
    async def curs(self) -> dict[int, str]:
        res = await self._coin_curs_pms()
        return {
            c["currencyId"]: c["nameShort"] for c in res["currency"]
        }  # if c['showPtoP'] todo: wht "showPtoP" is means

    # 22: Список платежных методов по каждой валюте
    async def cur_pms_map(self) -> dict[int, set[int]]:
        res = await self._coin_curs_pms()
        wrong_pms = {4, 34, 498, 548, 20009, 20010}  # , 212, 239, 363  # these ids not exist in pms
        return {c["currencyId"]: set(c["supportPayments"]) - wrong_pms for c in res["currency"] if c["supportPayments"]}

    async def coins(self) -> dict[int, str]:
        coins: list[dict] = (await self._coin_curs_pms())["coin"]
        return {c["coinId"]: c["coinCode"] for c in coins if c["coinType"] == 2}

    async def ads(self, coin: Coin, cur: Cur, is_sell: bool, pms: list[Pm] = None) -> list[Ad]:
        res = await self._coin_curs_pms()
        return res["country"]

    # Get all: currency,pay,allCountry,coin
    async def _coin_curs_pms(self) -> (dict, dict, dict, dict):
        res = await self._get("/-/x/otc/v1/data/config-list?type=currency,pay,coin")  # ,allCountry
        return res["data"]


async def main():
    _ = await init_db("postgres://artemiev:@/af_", models, True)
    ex = await Ex.get(name="Htx")
    cl = Client(ex)
    await cl.set_pmcurexs()
    await cl.set_coinexs()
    await cl.close()


run(main())
