from x_model import init_db
from xync_client.loader import DSN, BKEY, BSEC
from xync_schema import models
from xync_schema.models import Ex

from xync_client.Binance.ex import Client


async def test_cur_filter():
    _ = await init_db(DSN, models, True)
    ex = await Ex.get(name="Binance")
    bn = Client(ex, (BKEY, BSEC))
    resp = await bn.cur_pms_map()
    assert len(resp[0]) and len(resp[1]), "No data"
