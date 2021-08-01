import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from path import *

USERPATH = ""
USERDATA = ""
ALLPREVIOUS = ""

BARCHART = ""
PIECHART = ""
LINECHART = ""

dic = {"choice-question": "选择题",
       "true/false-question": "判断题",
       "fill-in-blank-question": "填空题",
       "short-answer-question": "简答题"}


def initUserPath():
    f = open(WORKINGUSR, 'r')
    usrname, pwd, uid = f.readline().split()
    global USERPATH, USERDATA, ALLPREVIOUS
    global BARCHART, PIECHART, LINECHART
    USERPATH = USERINF + uid + '/'
    USERDATA = USERPATH + 'data.txt'
    ALLPREVIOUS = USERPATH + 'allPrevious.txt'

    BARCHART = USERPATH + 'barChart.jpg'
    PIECHART = USERPATH + 'pieChart.jpg'
    LINECHART = USERPATH + 'lineChart.jpg'
    f.close()


def drawBarChart():
    Qtype = []
    rate = []
    try:
        total = 0
        with open(USERDATA, 'r') as data:
            for line in data.readlines():
                infs = line.split()
                Qtype.append(infs[0])

                total += int(infs[2])
                if int(infs[1]) == 0 and int(infs[2]) == 0:
                    infs[2] = '1'
                rate.append(int(infs[1]) / int(infs[2]))

        if total == 0:
            raise ZeroDivisionError

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

        global dic
        for i in range(len(Qtype)):
            Qtype[i] = dic[Qtype[i]]

        sns.barplot(x=Qtype, y=rate)
        plt.ylabel("正确率")
        plt.savefig(BARCHART)
        plt.close()
    except ZeroDivisionError:
        pass


def drawPieChart():
    Qtype = []
    cnt = []
    try:
        total = 0
        with open(USERDATA, 'r') as data:
            for line in data.readlines():
                infs = line.split()
                total += int(infs[2])
                if int(infs[2]) != 0:
                    Qtype.append(infs[0])
                    cnt.append(int(infs[2]))

        if total == 0:
            raise ZeroDivisionError

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

        global dic
        for i in range(len(Qtype)):
            Qtype[i] = dic[Qtype[i]]

        plt.pie(x=cnt, labels=Qtype, autopct='%1.2f%%')
        plt.title(f"总题数：{total}")

        plt.savefig(PIECHART)
        plt.close()
    except ZeroDivisionError:
        pass


def drawLineChart():
    cnt = []
    rate = []
    try:
        with open(ALLPREVIOUS, 'r') as data:
            for line in reversed(data.readlines()):
                infs = line.split()
                if len(cnt) == 6 or infs[0] == '0':
                    break
                cnt.insert(0, infs[0])
                rate.insert(0, float(infs[1]))

        if len(cnt) < 4:
            raise ZeroDivisionError

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

        for i in range(len(cnt)):
            cnt[i] = f"第{cnt[i]}次"

        df = pd.DataFrame({"次数": cnt, "正确率": rate})
        sns.lineplot(x="次数", y="正确率", data=df)

        plt.savefig(LINECHART)
        plt.close()
    except ZeroDivisionError:
        pass


def drawCharts():
    initUserPath()
    drawBarChart()
    drawPieChart()
    drawLineChart()
