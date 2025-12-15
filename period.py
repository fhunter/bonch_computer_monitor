"""Helper module for rrd utilities"""


def period_conv(period):
    """Converts period string to rrd's period argument"""
    return f"-1{period}"
