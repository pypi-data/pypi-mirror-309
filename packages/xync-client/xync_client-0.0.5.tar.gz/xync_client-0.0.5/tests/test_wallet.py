from asyncio import AbstractEventLoop, get_running_loop

import pytest
import uvloop
from tortoise import connections
from tortoise.backends.asyncpg import AsyncpgDBClient
from x_model import init_db
from xync_schema import models
from xync_schema.models import Agent, ExAction, TestEx

from xync_client.TgWallet.agent import AgentClient
from xync_client.TgWallet.ex import PublicClient
from xync_client.loader import DSN


@pytest.mark.asyncio(loop_scope="class")
class TestWallet:
    loop: AbstractEventLoop

    @pytest.fixture(scope="class")
    def event_loop_policy(self):
        return uvloop.EventLoopPolicy()

    @pytest.fixture(scope="class")
    async def cn(self) -> AsyncpgDBClient:
        TestWallet.loop = get_running_loop()
        await init_db(DSN, models, True)
        cn: AsyncpgDBClient = connections.get("default")
        yield cn
        await cn.close()

    @pytest.fixture(scope="class")
    async def ac(self, cn) -> AgentClient:
        agent = await Agent.get(user_id=1038938370).prefetch_related("ex")
        tg = AgentClient(agent)
        yield tg
        await tg.close()

    @pytest.fixture(scope="class")
    async def pc(self, cn) -> PublicClient:
        agent = await Agent.get(user_id=1038938370).prefetch_related("ex")
        tg = PublicClient(agent)
        yield tg
        await tg.close()

    # # 5 - fiats
    # async def test_fiats(self, ac):
    #     fiats = await ac.my_fiats()
    #     await TestEx.update_or_create({"ok": fiats['status'] == 'SUCCESS'}, ex__name=ac.agent.ex.name, action=ExAction.fiats)
    #     assert fiats['status'] == 'SUCCESS', "Failed to get fiats"

    # 1 - all_curs
    async def test_all_curs(self, pc):
        curs = await pc.curs()
        await TestEx.update_or_create({"ok": bool(curs)}, ex__name="TgWallet", action=ExAction.all_curs_taker)
        assert curs, "No data"

    # 2 - all_coins
    async def test_all_coins(self, pc):
        coins = await pc.coins()
        await TestEx.update_or_create({"ok": bool(coins)}, ex__name="TgWallet", action=ExAction.all_coins)
        assert coins, "No data"

    # 3 - all_pms
    async def test_all_pms(self, pc):
        pms = await pc.pms()
        await TestEx.update_or_create({"ok": bool(pms)}, ex__name="TgWallet", action=ExAction.all_pms)
        assert pms, "No data"

    # # 4 - all_ads
    # async def test_cur_filter(self, pc):
    #     for cur in 'RUB', 'AZN', 'GEL':
    #         for coin in 'TON', 'USDT', 'BTC':
    #             for tt in 'SALE', 'PURCHASE':
    #                 ads = await pc.get_ads(coin, cur, tt)
    #                 assert len(ads), "No data"
    #     await TestEx.update_or_create({"ok": bool(ads)}, ex__name="TgWallet", action=ExAction.all_ads)
    #
    # # 6 - fiat_new
    # async def test_fiat_new(self, ac):
    #     pms = await ac.all_pms()
    #     add_pm = await ac.fiat_new(pms[0]['code'], 'RUB', pms[0]['name'], '123456789098765')
    #     await TestEx.update_or_create({"ok": add_pm['status'] == 'SUCCESS'}, ex__name="TgWallet",
    #                                   action=ExAction.fiat_new)
    #     assert add_pm['status'] == 'SUCCESS', "Failed to create"
    #
    # # 7 - fiat_edit
    # async def test_fiat_edit(self, ac):
    #     editid = await ac.fiats()
    #     pms = await ac.all_pms()
    #     add_pm = await ac.fiat_edit(editid['data'][0]['id'], pms[0]['code'], 'RUB', pms[0]['name'], '9876543214442')
    #     await TestEx.update_or_create({"ok": add_pm['status'] == 'SUCCESS'}, ex__name="TgWallet",
    #                                   action=ExAction.fiat_upd)
    #     assert add_pm['status'] == 'SUCCESS', "Failed to edit"
    #
    # # 8 - fiat_del
    # async def test_fiat_del(self, ac):
    #     delid = await ac.fiats()
    #     dl = await ac.fiat_del(delid['data'][0]['id'])
    #     await TestEx.update_or_create({"ok": dl['status'] == 'SUCCESS'}, ex__name="TgWallet", action=ExAction.fiat_del)
    #     assert dl['status'] == "SUCCESS", "Fiat doesn't delete"
    #
    # # 9 - my_ads
    # async def test_my_ads(self, ac):
    #     ads = await ac.my_ads()
    #     await TestEx.update_or_create({"ok": ads['status'] == 'SUCCESS'}, ex__name="TgWallet", action=ExAction.my_ads)
    #     assert ads['status'] == "SUCCESS", "No data"
    #
    # # 10 - ad_new
    # async def test_ad_new(self, ac):
    #     fiats = [(await ac.fiats())['data'][0]['id']]
    #     ad = await ac.ad_new(fiats=fiats, amount=1000, coin="NOT", cur="EGP", tt="SALE")
    #     await TestEx.update_or_create({"ok": ad['status'] == 'SUCCESS'}, ex__name="TgWallet", action=ExAction.ad_new)
    #     assert ad['status'] == "SUCCESS", "No data"
    #
    # # 11 - ad_upd
    # async def test_ad_upd(self, ac):
    #     fiats = [(await ac.fiats())['data'][0]['id']]
    #     ad = (await ac.my_ads())['data'][0]
    #     upd = await ac.ad_upd(ad['type'], ad['id'], fiats, 1000)
    #     await TestEx.update_or_create({"ok": upd['status'] == 'SUCCESS'}, ex__name="TgWallet", action=ExAction.ad_upd)
    #     assert upd['status'] == "SUCCESS", "No data"
    #
    # # 13, 14 - ad_on/ad_off
    # async def test_ad_off_on(self, ac):
    #     ad = (await ac.my_ads())["data"][0]
    #     if ad['status'] == "ACTIVE":
    #         resulst_off = await ac.ad_off(ad['type'], ad['id'])
    #         assert resulst_off['status'] == "SUCCESS", "Inactivate failed"
    #     resulst_on = await ac.ad_on(ad['type'], ad['id'])
    #     assert resulst_on['status'] == "SUCCESS", "Activate failed"
    #     await TestEx.update_or_create({"ok": resulst_on['status'] == 'SUCCESS'}, ex__name="TgWallet",
    #                                   action=ExAction.ad_on)
    #     resulst_off = await ac.ad_off(ad['type'], ad['id'])
    #     await TestEx.update_or_create({"ok": resulst_off['status'] == 'SUCCESS'}, ex__name="TgWallet",
    #                                   action=ExAction.ad_off)
    #     assert resulst_off['status'] == "SUCCESS", "Inactivate failed"
    #
    # # 12 - ad_del
    # async def test_ad_del(self, ac):
    #     ad = (await ac.my_ads())['data'][0]
    #     ad_del = await ac.ad_del(ad['type'], ad['id'])
    #     await TestEx.update_or_create({"ok": ad_del['status'] == 'SUCCESS'}, ex__name="TgWallet",
    #                                   action=ExAction.ad_del)
    #     assert ad_del['status'] == "SUCCESS", "No data"
    #
    # # 15 - order_approve
    # async def test_order_approve(self, ac):
    #     orders = await ac.my_orders()
    #     agent = await Agent.get(user_id=2093307892)
    #     tgw = Private(agent)
    #     kyc = await tgw.get_kyc()
    #     if orders['data'][0]['seller']['userId'] == kyc:
    #         typ = 'SALE'
    #     elif orders['data'][0]['buyer']['userId'] == kyc:
    #         typ = 'BUY'
    #     else:
    #         typ = None
    #     approved = await ac.order_approve(orders['data'][0]['id'], typ)
    #     assert approved['status'] == "SUCCESS", "No approved"
    #
    # # 16 - order_reject
    # async def test_order_reject(self, ac):
    #     orders = await ac.my_orders()
    #     assert len(orders['data']), "No orders. You need create at least one order at first!"
    #     order_reject = await ac.order_reject(orders['data'][0]['id'])
    #     await TestEx.update_or_create({"ok": order_reject['status'] == 'SUCCESS'}, ex__name="TgWallet",
    #                                   action=ExAction.order_reject)
    #     assert order_reject['status'] == "SUCCESS", "No data"
    #
    # # 19 - order_paid
    # async def test_upload_file_order_paid(self, ac):
    #     orders = await ac.my_orders()
    #     agent = await Agent.get(user_id=1038938370)
    #     tgw = Private(agent)
    #     kyc = await tgw.get_kyc()
    #     if orders['data'][0]['seller']['userId'] == kyc:
    #         typ = 'SALE'
    #     elif orders['data'][0]['buyer']['userId'] == kyc:
    #         typ = 'BUY'
    #     else:
    #         typ = None
    #     order_id = await ac.order_approve(orders['data'][0]['id'], typ)
    #     upload = await ac.upload_file(order_id, 'Screenshot_788.png')
    #     assert upload['status'] == "SUCCESS", "No upload"
    #     paid = await ac.order_paid(orders['data'][0]['id'], upload['data']['file'])
    #     assert paid['status'] == "SUCCESS", "No data"
    #
    # # 20 - order_payment_confirm
    # async def test_order_payment_confirm(self, ac):
    #     orders = await ac.my_orders()
    #     confirm = await ac.order_payment_confirm(orders['data'][0]['id'])
    #     assert confirm['status'] == "SUCCESS", "No confirm"
