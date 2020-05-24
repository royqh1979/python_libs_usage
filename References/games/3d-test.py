#

from easygraphics import *

# p1 = [0,0,0]
# p3 = [0,0,100]
# p2 = [100,0,0]
# p4 = [100,0,100]

p1 = [0,30,0]
p3 = [0,130,0]
p2 = [100,30,0]
p4 = [100,130,0]


camera = [50,80,-100]


width = 800
height = 600

# 注： d 是 摄像机到投影面（与z轴垂直，中心在（0，0）处）的规范距离 （ 即投影面的x,y坐标范围均规范（缩放）为(1,1)，按同比例缩放后 摄影机到投影面的距离)
d_x = camera[2] / width * 2
d_y = camera[2] / height * 2


def translate(v):
    """
    计算点到摄像机的距离
    :param v:
    :return:
    """
    x = v[0] - camera[0]
    y = v[1] - camera[1]
    z = v[2] - camera[2]
    print(x,y,z)
    return x,y,z

def project(v):
    """
    将点 投射到规范投影面上 （以到摄像机的z轴距离为缩放因子）
    注意，在摄像机后方的点应看不到（v[2]必须大于0）这里未加判断
    :param v:
    :return:
    """
    x = v[0]*d_x/v[2]
    y = v[1]*d_y/v[2]
    print(x,y)
    return x,y

def scale(v):
    """
    将规范投影面上的点 还原到屏幕上
    :param v:
    :return:
    """
    x = (width/2) * (1+v[0])
    y = (height/2) * (1+v[1])
    print(x,y)
    return x,y

def convert(v):
    v=translate(v)
    v=project(v)
    v=scale(v)
    return v

print("???")
def main():
    init_graph(width,height)

    np1=convert(p1)
    np3=convert(p3)
    line(*np1,*np3)

    np2 = convert(p2)
    np4=convert(p4)
    line(*np2,*np4)
    pause()


easy_run(main)
