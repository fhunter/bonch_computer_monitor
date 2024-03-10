""" Utility modules for templates and graphs """
import datetime

def time_to_color(time_value):
    """ Returns time color for report time """
    if time_value < 5:
        return "green"
    if time_value < 10:
        return "orange"
    return "grey"

def time_to_online(time_value):
    """ Returns computer status by last report time """
    if time_value < 5:
        return "Online"
    if time_value < 10:
        return "Delay"
    return "Offline"

def usage_percent(used, total):
    """ Calculates usage percent, while preventing division by zero """
    if total == 0:
        return 0
    return int(100.0*used/total)

def scratch_data(scrtch):
    """ Outputs scratch data string """
    if scrtch:
        free = int(scrtch[2]/(1024*1024*1024))
        total = int(scrtch[1]/(1024*1024*1024))
        return "%d/%d Гб" % (free, total)
    return "N/A"

def ansible_data(ansible):
    """ Generates ansible status string """
    if ansible:
        return """
        <font color="green">%s</font> /
        <font color="orange">%s</font> /
        <font color="black">%s</font> /
        <font color="red">%s</font>&nbsp
        %s""" % (ansible[1],
                 ansible[2],
                 ansible[3],
                 ansible[4],
                 str(datetime.datetime.fromtimestamp(ansible[0])))
    return "N/A"

def is_ansible_ok(ansible,last_report):
    """ ansible - tuple of ansible values, [0] - timestamp
    last_report - datetime
    """
    result = ""
    if ansible:
        delta = last_report - datetime.datetime.fromtimestamp(ansible[0])
        delta = delta / datetime.timedelta(hours=1)
        if delta >= 12:
            result = "Нет данных"
        if int(ansible[4]) > 0:
            result = "Ошибка!"
    return result


def expand_hostname(hostname):
    """ Appends .dcti.sut.ru to hostname if not present """
    if not hostname.endswith('.dcti.sut.ru'):
        hostname = hostname + '.dcti.sut.ru'
    return hostname

def period_to_days(period):
    """ Convert string [dwmy] to time in days. Used to decipher input parameter """
    if period == "d":
        return 1
    if period == "w":
        return 7
    if period == "m":
        return 30
    if period == "y":
        return 365
    return None

def get_graph_title(hostnames):
    """ Generate title for graph or multiple graphs """
    if isinstance(hostnames, str):
        title = hostnames
        hostnames = (hostnames,)
    else:
        title = hostnames[0]
        hostnames = hostnames[1:]
    return title, hostnames
