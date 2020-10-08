from datetime import datetime


def __date_log_format():
    return datetime.now().strftime("%H:%M")



def info_log(message):
    return "({date}) [INFO] > {message}".format(date=__date_log_format(), message=message)


def command_log(username, command):
    return "({date}) [COMMAND] {user} > {cmd}".format(date=__date_log_format(), user=username, cmd=command)


def error_log(message):
    return "({date}) [ERROR] > {message}".format(date=__date_log_format(), message=message)