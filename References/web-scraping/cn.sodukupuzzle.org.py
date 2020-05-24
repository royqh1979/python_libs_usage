#从cn.sodukupuzzle.org下载
from typing import List

from requests_html import HTMLSession,HTML,Element
import re
import datetime
import time
import random

years = range(2008,2020)
monthes = range(1,13)

def get_puzzle(session:HTMLSession,url:str):
    print(url)
    r = session.get(url)
    c = r.html
    contents = c.html
    match=re.search("tmda='([\\d]+)'",contents)
    start,end=match.span(1)
    tm=contents[start:start+81]
    da=contents[start+81:start+162]
    nd=contents[start+163]
    return tm,da,nd

session = HTMLSession()

d = datetime.date(2008, 1, 1)
today = datetime.date.today()
print(d, today, d < today, d + datetime.timedelta(days=100))

with open("sodukus.data","w",encoding="GBK") as file:
    file.write("level,puzzle,answer\n")
    while d < today:
        for l in range(5):
            time.sleep(1)
            tm,da,nd = get_puzzle(session,
                                  f"http://www.cn.sudokupuzzle.org/printable.php?nd={l}&y={d.year}&m={d.month}&d={d.day}")
            file.write(f"{nd},{tm},{da}\n")
            file.flush()
        d = d + datetime.timedelta(days=1)

# print(contents)


