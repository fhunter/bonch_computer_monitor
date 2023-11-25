""" Common module for round-robbin functions """

import rrdtool

def last(filename):
    last_time = None
    try:
        last_time = rrdtool.last(filename)
    except BaseException:
        return None
    return last_time

def latest(filename, data):
    try:
        info = rrdtool.info(filename)
        lastupdate = [info['last_update'],]
        for i in data:
            lastupdate.append(info[f'ds[{i}].last_ds'])
        return lastupdate
    except BaseException:
        return None
