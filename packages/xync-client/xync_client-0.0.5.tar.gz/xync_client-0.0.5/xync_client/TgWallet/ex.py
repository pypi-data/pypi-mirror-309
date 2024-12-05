import logging

from aiohttp import ClientResponse
from aiohttp.http_exceptions import HttpProcessingError
from x_client.http import Client
from xync_schema.models import Coin, Cur, Pm, Ad, Curex, Agent, Ex

from xync_client.Abc.Ex import ExClient
from xync_client.TgWallet.pyro import PyroClient


class PublicClient(ExClient):
    async def cur_pms_map(self) -> dict[int | str, list[int | str]]:
        pass

    def __init__(self, agent: Agent):
        self.agent: Agent = agent
        assert isinstance(agent.ex, Ex), "`ex` should be fetched in `agent`"
        assert agent.ex.host_p2p, "`ex.host_p2p` shouldn't be empty"
        self.meth = {
            "GET": self._get,
            "POST": self._post,
        }
        super().__init__(agent.ex)

    async def _get_auth_hdrs(self) -> dict[str, str]:
        pyro = PyroClient(self.agent)
        init_data = await pyro.get_init_data()
        # async with ClientSession(self.agent.ex.url_login) as sess:
        #     resp = await sess.post('/api/v1/users/auth/', data=init_data, headers={'content-type': 'application/json;charset=UTF-8'})
        #     tokens = await resp.json()
        tokens = Client("walletbot.me")._post("/api/v1/users/auth/", init_data)
        return {"Wallet-Authorization": tokens["jwt"], "Authorization": "Bearer " + tokens["value"]}

    async def login(self) -> None:
        auth_hdrs: dict[str, str] = await self._get_auth_hdrs()
        self.session.headers.update(auth_hdrs)

    async def _proc(self, resp: ClientResponse, data: dict = None) -> dict | str:
        try:
            return await super()._proc(resp)
        except HttpProcessingError as e:
            if e.code == 401:
                logging.warning(e)
                await self.login()
                res = await self.meth[resp.method](resp.url.path, data)
                return res

    async def _curs(self) -> list[str]:
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        return [c["code"] for c in coins_curs["data"]["fiat"]]

    async def curs(self) -> list[Cur.pyd()]:
        curs = [(await Cur.update_or_create(ticker=c))[0] for c in await self._curs()]
        [await Curex.update_or_create(cur=c, ex=self.agent.ex) for c in curs]  # add curexs
        return [Cur.pyd().model_validate(c, from_attributes=True) for c in curs]

    async def _coins(self) -> list[str]:
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        return [c["code"] for c in coins_curs["data"]["crypto"]]

    async def coins(self, cur: Cur = None) -> list[Coin.pyd()]:
        coins = [(await Coin.update_or_create(ticker=c))[0] for c in await self._coins()]
        [await Curex.update_or_create(coin=c, ex=self.agent.ex) for c in coins]  # add coinexs
        return [Coin.pyd().model_validate(c, from_attributes=True) for c in coins]

    async def _pms(self, cur: str = "RUB") -> list[Pm]:
        pms = await self._post("/p2p/public-api/v3/payment-details/get-methods/by-currency-code", {"currencyCode": cur})
        return pms["data"]

    async def pms(self, cur: str = "RUB") -> list[Pm]:
        # get from api
        pmcurs = {cur: await self._pms(cur) for cur in await self._curs()}
        pp = {}
        [[pp.update({p["code"]: p["nameEng"]}) for p in ps] for ps in pmcurs.values()]
        pp = {k: v for k, v in sorted(pp.items(), key=lambda x: x[0])}
        return pp
        # pms_new = await self._post(
        #     "/p2p/public-api/v3/payment-details/get-methods/by-currency-code", {"currencyCode": cur}
        # )
        # pms_new_idfs: dict[str, str] = {
        #     pn["code"]: pn["nameEng"].lower().replace(" ", "").replace("-", "") for pn in pms_new["data"]
        # }
        # pms_new_names = {name: idf for idf, name in pms_new_idfs.items()}
        # # prepare old payMeths
        # pms_old = await Pm.all()
        # pms_old_idfs: dict[str, Pm] = {
        #     pm.identifier.lower().replace(" ", "").replace("-", ""): pm for pm in pms_old if pm.identifier
        # }
        # pms_old_names: dict[str, Pm] = {
        #     pm.name.lower().replace(" ", "").replace("-", ""): pm for pm in pms_old if pm.name
        # }

    async def ads(self, coin: Coin, cur: Cur, is_sell: bool, pms: list[Pm] = None) -> list[Ad.pyd()]:
        params = {
            "baseCurrencyCode": coin,
            "quoteCurrencyCode": cur,
            "offerType": is_sell,
            "offset": 0,
            "limit": 100,
            # ,"merchantVerified":"TRUSTED"
        }
        ads = await self._post("/p2p/public-api/v2/offer/depth-of-market/", params)
        return ads
