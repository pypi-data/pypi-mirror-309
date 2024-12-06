#!/usr/bin/env python

import os


def create_path(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)




