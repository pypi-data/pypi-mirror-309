#!/usr/bin/env python
import logging
import time

from binance.cm_futures import CMFutures
from binance.lib.utils import config_logging

config_logging(logging, logging.DEBUG)

cm_futures_client = CMFutures(show_limit_usage=True)

logging.info(cm_futures_client.time())


