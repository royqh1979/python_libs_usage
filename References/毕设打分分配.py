import random

# MAX_SCORES = [30,20,30,15,5]
MAX_SCORES = [30,25,10,5,30]

def check_max_scores(MAX_SCORES):
    m = sum(MAX_SCORES)
    if m!=100:
        raise ValueError("总分必须为100")

try:
    score=int(input("请输入总分:"))
except:
    raise ValueError("总分必须为整数！")

random.seed()
n=len(MAX_SCORES)
scores = [0]*n


for i in range(n):
    scores[i] = score * MAX_SCORES[i] // 100

remain = score - sum(scores)

rnd_lst = list(range(n))
while remain>0:
    i=random.choice(rnd_lst)
    if MAX_SCORES[i]-scores[i]>=1:
        scores[i]+=1
        remain-=1

if sum(scores)!=score:
    raise RuntimeError("总分与所给不符！")

print(scores)








88