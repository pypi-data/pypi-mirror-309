import logging

from aiohttp import ClientResponse
from aiohttp.http_exceptions import HttpProcessingError
from x_client.http import Client
from xync_schema.models import Pm, Agent, Ex

from xync_client.Abc.Ex import ExClient
from xync_client.TgWallet.pyro import PyroClient


class PublicClient(ExClient):
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

    async def curs(self) -> dict[str, str]:
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        return {c["code"]: c["code"] for c in coins_curs["data"]["fiat"]}

    async def coins(self) -> dict[str, str]:
        coins_curs = await self._post("/p2p/public-api/v2/currency/all-supported")
        return {c["code"]: c["code"] for c in coins_curs["data"]["crypto"]}

    async def _pms(self, cur: str = "RUB") -> dict[str, dict]:
        pms = await self._post("/p2p/public-api/v3/payment-details/get-methods/by-currency-code", {"currencyCode": cur})
        return {pm["code"]: {"name": pm["nameEng"]} for pm in pms["data"]}

    async def pms(self) -> dict[str, dict]:
        pms = {}
        for cur in await self.curs():
            for k, pm in (await self._pms(cur)).items():
                pms.update({k: pm})
        return pms

    async def cur_pms_map(self) -> dict[str, list[str]]:
        return {cur: list(await self._pms(cur)) for cur in await self.curs()}

    async def ads(self, coin: str, cur: str, is_sell: bool, pms: list[Pm] = None) -> list[dict]:
        params = {
            "baseCurrencyCode": coin,
            "quoteCurrencyCode": cur,
            "offerType": "SALE" if is_sell else "PURCHASE",
            "offset": 0,
            "limit": 10,
            # ,"merchantVerified":"TRUSTED"
        }
        ads = await self._post("/p2p/public-api/v2/offer/depth-of-market/", params)
        return ads
