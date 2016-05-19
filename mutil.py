# coding: utf-8


import json
import os
import logging
import logging.handlers


def loadJsonData(filename):
    '''
    加载json文件中的数据
    :param filename:
    :return: python对象
    '''
    assert os.path.exists(filename), '%s do not exists' % filename

    data = None
    with open(filename) as f:
        data = json.load(f)

    return data

def dumpJsonData(filename, data):
    '''
    将数据保存到json文件中
    '''
    dataDir = os.path.split(filename)[0]
    if dataDir == '':
        dataDir = '.'
    assert os.path.exists(dataDir), '%s directory do not exists' % dataDir

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def setUpLog(logName):
    logger = logging.getLogger(logName)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logFile = '%s.log' % logName if logName != '' else 'root.log'

    fileHandler = logging.handlers.RotatingFileHandler(
        logFile, maxBytes=(1048576 * 5), backupCount=7
    )
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
