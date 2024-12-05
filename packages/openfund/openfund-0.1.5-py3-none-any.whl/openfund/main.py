import sys

from openfund.binance_tools import *
from openfund.libs.log_tools import Logger


print(sys.version)
app = "main"
logger = Logger(app).get_log()
logger.info("main Starting ...... ")
logger.info("binance_tools: %s" % get_time())
logger.info("binance_tools: %s" % get_account())
