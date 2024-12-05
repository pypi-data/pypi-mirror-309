#!/usr/bin/env python

import os
import pathlib
from configparser import ConfigParser

config = ConfigParser()
config_file_path = os.path.join(
    pathlib.Path(__file__).parent.resolve(), "..", "config.ini"
)
config.read(config_file_path)


def get_api_key():

    return config["keys"]["api_key"], config["keys"]["api_secret"]


def get_path():
    return config["path"]["data_path"], config["path"]["log_path"]


def get_mail():
    return (
        config["mail"]["email_address"],
        config["mail"]["email_password"],
        config["mail"]["email_receiver"],
    )
