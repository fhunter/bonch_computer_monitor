import datetime

def time_to_color(time_value):
    if time_value < 5:
        return "green"
    if time_value < 10:
        return "orange"
    return "grey"

def time_to_online(time_value):
    if time_value < 5:
        return "Online"
    if time_value < 10:
        return "Delay"
    return "Offline"

def usage_percent(used, total):
    if total == 0:
        return 0
    return int(100.0*used/total)

def scratch_data(scrtch):
    if scrtch:
        free = int(scrtch[2]/(1024*1024*1024))
        total = int(scrtch[1]/(1024*1024*1024))
        return "%d/%d Гб" % (free, total)
    return "N/A"
        
def ansible_data(ansible):
    if ansible:
        return """
        <font color="green">%d</font> /
        <font color="orange">%d</font> /
        <font color="black">%d</font> /
        <font color="red">%d</font>&nbsp
        %s""" % (ansible[1], ansible[2], ansible[3], ansible[4], str(datetime.datetime.fromtimestamp(ansible[0])))
    return "N/A"
