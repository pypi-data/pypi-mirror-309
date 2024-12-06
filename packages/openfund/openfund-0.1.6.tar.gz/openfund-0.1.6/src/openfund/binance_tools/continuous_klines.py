#!/usr/bin/env python
import csv
import logging
import time

from datetime import datetime

from binance.um_futures import UMFutures
from binance.um_futures import UMFutures
from binance.error import ClientError

from openfund.libs.time_tools import format_timestamp
from openfund.libs.file_tools import create_path
from openfund.libs.prepare_env import get_api_key, get_path
from openfund.libs import enums

# 数据路径、日志路径
data_path, log_path = get_path()
# client
um_futures_client = UMFutures()
# 合同类型
contractTypes = [type.value for type in enums.ContractType]
# 币种类型
# POOL = enums.CUR_SYMBOL_POOL
POOL = [
    "BTCUSDT_240329",
    "BLURUSDT",
    "DYDXUSDT",
    "ETHBTC",
    "ETHBUSD",
    "ETHUSDT",
    "ETHUSDT_231229",
    "ETHUSDT_240329",
    "GMTBUSD",
    "GMTUSDT",
    "LTCBUSD",
    "LTCUSDT",
    "MATICBUSD",
    "MATICUSDT",
    "SOLBUSD",
    "SOLUSDT",
]
interval = enums.KLINE_INTERVAL_5MINUTE
limit = 1500
errorLimit = 100
sleepSec = 10

# 历史截止数据开关
hisSwitch = 0
# hisSwitch 打开的情况下，抓取数据截止时间
hisDateTime = 1653974399999

for symbol in POOL:
    fileName = "{}/continuous_klines_{}_{}.log".format(
        log_path, symbol, format_timestamp(datetime.now().timestamp() * 1000)
    )
    # print(fileName)
    logging.basicConfig(
        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        filename=fileName,
    )
    logging.info("{} symbol 开始 ++++++++++++++++++++++++++++ ".format(symbol))
    total = 0
    for contractType in contractTypes:
        latestRecords = 1
        records = 0  # 累计记录数
        queryTimes = 0  # 执行次数
        nextEndTime = 0
        errorCount = 0
        params = {"limit": limit}
        while latestRecords != 0:  # 循环读取，直到记录为空
            queryTimes = queryTimes + 1
            if nextEndTime != 0:
                params = {"limit": limit, "endTime": nextEndTime}

            logging.info(
                "1、{}-{} 第{}次开始执行...".format(symbol, contractType, queryTimes)
            )
            listData = []
            try:
                listData = um_futures_client.continuous_klines(
                    symbol, contractType, interval, **params
                )
            except KeyError as err:
                print("KeyError:", err)
                logging.error(err)
                break
            except ClientError as error:
                logging.error(
                    "Found error. status: {}, error code: {}, error message: {}".format(
                        error.status_code, error.error_code, error.error_message
                    )
                )
                if error.error_code == -4144 and error.status_code == 400:
                    break
            except Exception as e:
                print("Error:", e)
                logging.error(e)
                errorCount = errorCount + 1
                if errorCount > errorLimit:
                    break
                else:
                    time.sleep(sleepSec)
                    continue

            latestRecords = len(listData)
            records = latestRecords + records
            logging.info("2、{}条写入文件...".format(latestRecords))

            path = "{}/continuous_klines/{}/{}/".format(data_path, symbol, contractType)
            create_path(path)  # 不存在路径进行呢创建

            with open(
                "{}continuous_klines_{}_{}_{}.csv".format(
                    path, symbol, contractType, interval
                ),
                "a",
                newline="",
            ) as file:
                writer = csv.writer(file)
                # 时间戳倒序，插入文件尾部
                writer.writerows(sorted(listData, key=lambda x: x[0], reverse=True))

            # 拿到最后一条记录后,获取close时间戳,变为下一次截止时间戳
            if latestRecords > 0:
                nextEndTime = (
                    listData[0][0] - 1
                )  # -1 不和close时间戳相同，避免重新拉取重复数据
                errorCount = 0
                logging.info(
                    "3、下次结束时间 {} {}".format(
                        format_timestamp(nextEndTime), nextEndTime
                    )
                )

                if nextEndTime <= hisDateTime and hisSwitch == 1:
                    break
            else:
                logging.info("4、结束...")

            total = total + records
            logging.info("5、{} 抓取数据 {} 条记录...".format(symbol, records))

    logging.info("6、{} 抓取数据 {} 条记录...".format(symbol, total))
    logging.info("{} symbol --------------------------------- ".format(symbol))
