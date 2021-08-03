import os

USERINF = "./usersInf/"
DATABASE = "./database/"
PICSRC = "./picSrc/"

USERLOG = USERINF + "users.csv"

UID = USERINF + "uid.txt"
WORKINGUSR = USERINF + "workingUsr.txt"


CHOICEQ = DATABASE + "choiceQ.xlsx"
JUDGEMENTQ = DATABASE + "judgementQ.xlsx"
SHORTANSQ = DATABASE + "shortAnsQ.xlsx"
FILLINBLANKQ = DATABASE + "fillinBlankQ.xlsx"

WCHOICEQ = DATABASE + "wchoiceQ.xlsx"
WJUDGEMENTQ = DATABASE + "wjudgementQ.xlsx"
WSHORTANSQ = DATABASE + "wshortAnsQ.xlsx"
WFILLINBLANKQ = DATABASE + "wfillinBlankQ.xlsx"


def initPath():
    createDir(USERINF)
    createFile(USERLOG)
    f = open(UID, 'w', encoding='utf-8')
    f.write("100000\n")
    f.close()


def createFile(filename):
    f = open(filename, 'w', encoding='utf-8')
    f.close()


def createDir(dirname):
    os.makedirs(dirname)


def writeSingleLine(filename, line):
    f = open(filename, 'w', encoding='utf-8')
    f.write(line)
    f.close()

