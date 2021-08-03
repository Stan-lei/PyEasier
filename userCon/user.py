from path import *


def hasUser(username):
    with open(USERLOG, 'r', encoding='utf-8') as f:
        f.seek(0)
        for line in f.readlines():
            if username == line.split()[0]:
                f.close()
                return True
        f.close()
        return False


def getUser(username):
    with open(USERLOG, 'r', encoding='utf-8') as f:
        f.seek(0)
        for line in f.readlines():
            if username == line.split()[0]:
                f.close()
                return line
        f.close()
        return None
