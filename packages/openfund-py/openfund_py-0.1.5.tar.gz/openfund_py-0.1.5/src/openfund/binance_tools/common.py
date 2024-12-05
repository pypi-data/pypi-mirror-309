# common.py

from binance.spot import Spot as Client

from openfund.libs.log_tools import Logger
from openfund.libs.prepare_env import get_api_key

app = "binance_tools"
api_key, api_secret = get_api_key()

client = Client(api_key, api_secret)


def get_time():
    logger = Logger(app).get_log()
    logger.info("binance_tools.get_time Starting ...... ")
    # print(say_hello("John"))
    return client.time()


def get_account():
    logger = Logger(app).get_log()
    logger.info("binance_tools.get_accont Starting ...... ")
    return client.account()


# print(get_time())
