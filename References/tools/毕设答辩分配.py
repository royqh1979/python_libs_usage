from typing import Set, Dict

import pandas as pd
from dataclasses import dataclass
import random


@dataclass
class Teacher:
    name: str
    students: Set[str]
    group: int

teachers : Dict[str,Teacher] = {}
reviews = {}
students = {}
groups = {}
with open("导师分配.csv","r",encoding="GBK") as file:
    df = pd.read_csv(file)

for index,row in df.iterrows():
    t_name  = row['导师']
    s_name = row['姓名']
    if t_name not in reviews:
        reviews[t_name] = set()
    t = teachers.get(t_name,Teacher(t_name,set(),0))
    t.students.add(s_name)
    teachers[t_name] = t

    students[s_name] = t_name


with open("导师分组.csv", "r", encoding="GBK") as file:
    df = pd.read_csv(file)
for index,row in df.iterrows():
    t_name = row['教师']
    group = int(row['组别'])
    teachers[t_name].group = group
    g = groups.get(group,set())
    g.add(t_name)
    groups[group]=g

print(students)
print(groups)

st={}
for s_name in students:
    t_name = students[s_name]
    while True:
        g=random.randint(1,4)
        if t_name not in groups[g]:
            break
    st[s_name]=g

with open("分配结果.csv","w",encoding="GBK") as file:
    file.write("姓名,指导教师,答辩组\n")
    for s_name in students:
        file.write(f"{s_name},{students[s_name]},{st[s_name]}\n")

