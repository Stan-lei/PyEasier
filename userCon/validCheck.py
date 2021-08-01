import re


def checkUA(text):
    if re.search("^[0-9A-Za-z\u4E00-\u9FA5_]{3,12}$", text):
        return True
    else:
        return False


def checkPwd(text):
    if re.search("^[0-9A-Za-z_]{6,18}$", text):
        return True
    else:
        return False
