import logging
from abc import abstractmethod

from aiohttp import ClientResponse
from aiohttp.http_exceptions import HttpProcessingError
from x_client.aiohttp import Client
from xync_schema.enums import PmType
from xync_schema.models import Agent, Ex, User, OrderStatus, Coin, Cur, Order, Pm, Ad, AdStatus, Fiat


class AgentClient(Client):
    def __init__(self, agent: Agent):
        self.agent: Agent = agent
        assert isinstance(agent.ex, Ex), "`ex` should be fetched in `agent`"
        assert agent.ex.host_p2p, "`ex.host_p2p` shouldn't be empty"
        self.meth = {
            "GET": self._get,
            "POST": self._post,
        }
        super().__init__(agent.ex.host_p2p)

    # -1: Login: returns auth headers dict
    @abstractmethod
    async def _get_auth_hdrs(self) -> dict[str, str]: ...

    async def login(self) -> None:
        auth_hdrs: dict[str, str] = await self._get_auth_hdrs()
        self.session.headers.update(auth_hdrs)

    # 0: Получшение ордеров в статусе status, по монете coin, в валюте coin, продаже(is_sell=True)/покупке(is_sell=False)
    @abstractmethod
    async def get_orders(
        self, stauts: OrderStatus = OrderStatus.active, coin: Coin = None, cur: Cur = None, is_sell: bool = None
    ) -> list[Order]: ...

    # 1: [T] Получшение ордеров в статусе status, по монете coin, в валюте coin, продаже(is_sell=True)/покупке(is_sell=False)
    @abstractmethod
    async def order_request(self, ad_id: int, amount: float) -> Order: ...

    # async def start_order(self, order: Order) -> OrderOutClient:
    #     return OrderOutClient(self, order)

    # # # Fiat
    # 25: Список реквизитов моих платежных методов
    @abstractmethod
    async def my_fiats(self, cur: Cur = None) -> list[Fiat.pyd()]: ...

    # 26: Создание
    @abstractmethod
    async def fiat_new(self, fiat: Fiat.pyd()) -> Fiat.pyd(): ...

    # 27: Редактирование
    @abstractmethod
    async def fiat_upd(self, detail: str = None, type_: PmType = None) -> bool: ...

    # 28: Удаление
    @abstractmethod
    async def fiat_del(self, fiat_id: int) -> bool: ...

    # # # Ad
    # 29: Список моих ad
    @abstractmethod
    async def my_ads(self) -> list[Ad]: ...

    # 30: Создание ad:
    @abstractmethod
    async def ad_new(
        self,
        coin: Coin,
        cur: Cur,
        is_sell: bool,
        pms: list[Pm],
        price: float,
        is_float: bool = True,
        min_fiat: int = None,
        details: str = None,
        autoreply: str = None,
        status: AdStatus = AdStatus.active,
    ) -> Ad: ...

    # 31: Редактирование
    @abstractmethod
    async def ad_upd(
        self,
        pms: [Pm] = None,
        price: float = None,
        is_float: bool = None,
        min_fiat: int = None,
        details: str = None,
        autoreply: str = None,
        status: AdStatus = None,
    ) -> bool: ...

    # 32: Удаление
    @abstractmethod
    async def ad_del(self) -> bool: ...

    # 33: Вкл/выкл объявления
    @abstractmethod
    async def ad_switch(self) -> bool: ...

    # 34: Вкл/выкл всех объявлений
    @abstractmethod
    async def ads_switch(self) -> bool: ...

    # # # User
    # 35: Получить объект юзера по его ид
    @abstractmethod
    async def get_user(self, user_id) -> User: ...

    # 36: Отправка сообщения юзеру с приложенным файло
    @abstractmethod
    async def send_user_msg(self, msg: str, file=None) -> bool: ...

    # 37: (Раз)Блокировать юзера
    @abstractmethod
    async def block_user(self, is_blocked: bool = True) -> bool: ...

    # 38: Поставить отзыв юзеру
    @abstractmethod
    async def rate_user(self, positive: bool) -> bool: ...

    async def _proc(self, resp: ClientResponse, data: dict = None) -> dict | str:
        try:
            return await super()._proc(resp)
        except HttpProcessingError as e:
            if e.code == 401:
                logging.warning(e)
                await self.login()
                res = await self.meth[resp.method](resp.url.path, data)
                return res

    @staticmethod
    async def payment_methods(*methods_list):
        payment_list = []
        for method in methods_list:
            method_cleared = method.lower().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            if method_cleared not in payment_list:
                payment_list.append(method_cleared)
        return payment_list
