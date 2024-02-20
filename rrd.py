""" Common module for round-robbin functions """

import rrdtool

def create(filename,data_limits):
    """ data_limits - list of pairs of [name, max_value] """
    arglist = (filename, "--start", '-2years', '--step', '900')
    for i in data_limits:
        arglist = arglist + (f"DS:{i[0]}:GAUGE:1200:0:{i[1]}",)
    arglist = arglist + ('RRA:AVERAGE:0.5:1:1200',
                         'RRA:AVERAGE:0.5:6:1200',
                         'RRA:AVERAGE:0.5:24:1200',
                         'RRA:MIN:0.5:1:1200',
                         'RRA:MIN:0.5:6:1200',
                         'RRA:MIN:0.5:24:1200',
                         'RRA:MAX:0.5:1:1200',
                         'RRA:MAX:0.5:6:1200',
                         'RRA:MAX:0.5:24:1200',
                         'RRA:LAST:0.5:1:1200',
                         'RRA:LAST:0.5:6:1200',
                         'RRA:LAST:0.5:24:1200')
    rrdtool.create(*arglist)

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
