import random
import pandas as pd
from path import *


def randomCQ(n):
    return randomQ(n, CHOICEQ)


def randomJQ(n):
    return randomQ(n, JUDGEMENTQ)


def randomFBQ(n):
    return randomQ(n, FILLINBLANKQ)


def randomSAQ(n):
    return randomQ(n, SHORTANSQ)


def randomQ(n, path):
    df = pd.read_excel(path)
    total = df.shape[0] + 1
    if n > total:
        n = total - 1
    nums = random.sample(range(1, total), n)
    questions = []
    for n in nums:
        questions.append(df[n - 1:n])
    return questions
