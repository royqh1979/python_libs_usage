"""
数独求解

使用简化的启发式回溯搜索

使用递归实现

每次优先尝试填写可行数字最少的格子

"""
import numpy as np
from easygraphics import *
from dataclasses import dataclass
import copy
from typing import Set

FONT_WIDTH = 30
BOARD_TOP = 10
BOARD_LEFT = 10
SQUARE_WIDTH = 50

SPEED = 100

# 棋盘，为了方便定义为[10][10]，实际只用[1][1]-[9][9]
board = np.zeros((10, 10),dtype="int32")

# 行、列、小九宫已使用数字集合
cols = [set() for i in range(10)]  # 各列数字集合
rows = [set() for i in range(10)]  # 各行数字集合
blks = [set() for i in range(10)]  # 各小九宫格数字集合

# 绘图相关函数
def draw_number_at(i, j, number, color):
    """
    Draw a number at cell(i,j) with the specified color
    :param i: the row
    :param j: the column
    :param number: the number
    :param color: the color
    """
    left = BOARD_LEFT + (j - 1) * SQUARE_WIDTH
    top = BOARD_TOP + (i - 1) * SQUARE_WIDTH
    set_color(color)
    if number != 0:
        draw_rect_text(left + 5, top + 5, FONT_WIDTH, FONT_WIDTH, number)
    else:
        set_color(Color.WHITE)
        fill_rect(left+1, top+1, left + SQUARE_WIDTH-2, top + SQUARE_WIDTH-2)


def draw_board():
    clear_device()
    for i in range(1, 10):
        for j in range(1, 10):
            left = BOARD_LEFT + (j - 1) * SQUARE_WIDTH
            top = BOARD_TOP + (i - 1) * SQUARE_WIDTH
            set_color(Color.LIGHT_GRAY)
            rect(left, top, left + SQUARE_WIDTH, top + SQUARE_WIDTH)
            draw_number_at(i, j, board[i][j], Color.RED)

    # 画小九宫格边框
    set_color(Color.BLACK)
    for i in range(1, 4):
        for j in range(1, 4):
            left = BOARD_LEFT + (j - 1) * 3 * SQUARE_WIDTH
            top = BOARD_TOP + (i - 1) * 3 * SQUARE_WIDTH
            rect(left, top, left + 3 * SQUARE_WIDTH, top + 3 * SQUARE_WIDTH)


def init():
    init_graph(800, 600)
    set_color(Color.BLACK)
    set_background_color(Color.WHITE)
    set_line_width(2)
    set_fill_color(Color.WHITE)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_font_size(FONT_WIDTH)


DATA_FILE = "10soduku.board"


# 候选格子, canPut[n]=1表示该格可以放数字n，否则不行
@dataclass()
class CandiateSquare:
    x: int = 0
    y: int = 0
    possibles = set()


def which_block(i, j):
    """
    计算当前方格属于哪一宫

    :param i: 格子所在行
    :param j: 格子所在列
    :return: 格子所在的宫编号
    """
    return ((i - 1) // 3) * 3 + ((j - 1) // 3)+1


def tag(i, j, number):
    """
    在本列、本行、本宫中标记数字number已被使用

    :param i: 格子所在的行
    :param j: 格子所在的列
    :param number: 格子中填写的数字
    """
    rows[i].add(number)
    cols[j].add(number)
    block = which_block(i,j)
    blks[block].add(number)


def untag(i, j, number):
    """
    在本列、本行、本宫中取消数字val的使用标记

    :param i: 格子所在的行
    :param j: 格子所在的列
    :param number: 格子中填写的数字
    """
    rows[i].remove(number)
    cols[j].remove(number)
    block = which_block(i,j)
    blks[block].remove(number)


def fill(i, j, number):
    """
    将数字val填写到方格(i,j)中

    :param i: 格子所在的行
    :param j: 格子所在的列
    :param number: 格子中填写的数字
    """
    board[i][j] = number
    tag(i, j, number)


def unfill(i, j):
    """
    清除方格(i,j)中的数字

    :param i: 格子所在的行
    :param j: 格子所在的列
    """

    number = board[i][j]
    untag(i, j, number)
    board[i][j] = 0


def load_board(boardFile):
    """
    从数据文件中读取数独初始状态

    :param boardFile: 数据文件名
    """
    global board
    try:
        with open(boardFile, mode="r") as file:
            board = [ [0]*10 for i in range(10)]
            for line in file:
                line = line.strip()
                numbers = line.split(',')
                if len(numbers) != 3:
                    continue
                i, j, k = int(numbers[0]), int(numbers[1]), int(numbers[2])
                board[i][j] = k
    except IOError :
        clear_device()
        draw_rect_text(10, 500, 700, 50, f"无法打开文件{boardFile}")


def count_unsolved():
    """
    计算有多少个格子需要填

    :return:
    """
    count = 0
    for i in range(1, 10):
        for j in range(1, 10):
            if board[i][j] == 0:
                count += 1
    return count


def can_fill(i, j, number):
    """
    判断number能否填写在格子(i,j)中

    :param i: 格子所在的行
    :param j: 格子所在的列
    :param number: 要填写的数字
    """
    if number in rows[i]:
        return False
    if number in cols[j]:
        return False
    if number in blks[which_block(i, j)]:
        return False
    return True


def calculatePossible(i, j):
    """
    找出格子（i,j）中所有可填的数字

    :param i: 格子所在的行
    :param j: 格子所在的列
    """
    possibles = set()
    for number in range(1, 10):
        if can_fill(i, j, number):
            possibles.add(number)
    return possibles

def findSureSquareByBlock():
    """
    排除法1：对于每一个数字，在每一个九宫看看它是否只有一个可填位置
    """
    for number in range(1,10):
        in_rows = copy.deepcopy(rows)
        in_cols = copy.deepcopy(cols)
        in_blks = copy.deepcopy(blks)
        while True:
            # print(in_rows)
            # print(in_cols)
            # print(in_blks)
            found_one_row = False # 发现数字number只能在某九宫的某行上
            found_one_col = False # 发现数字number只能在某九宫的某列上
            for block in range(1,10):
                if number not in in_blks[block]:
                    start_row = ((block-1) // 3 ) * 3 + 1
                    start_col = (block-1) % 3 * 3 +1
                    if block != which_block(start_row,start_col):
                        print(number,block,start_row,start_col,which_block(start_row,start_col))
                    can_rows = [] # 数字number能填在该九宫的哪几行
                    can_cols = [] # 数字number能填在该九宫的哪几列
                    for i in range(3):
                        for j in range(3):
                            row=start_row+i
                            col=start_col+j
                            if (board[row][col]==0) and (number not in in_rows[row]) and (number not in in_cols[col]):
                                if row not in can_rows:
                                    can_rows.append(row)
                                if col not in can_cols:
                                    can_cols.append(col)
                    # print(number,block,can_rows,can_cols)

                    if len(can_rows)==1 and len(can_cols)==1: #只能填在某行某格上
                        row=can_rows[0]
                        col=can_cols[0]
                        return number,row,col
                    if len(can_rows)==1:
                        found_one_row = True
                        row = can_rows[0]
                        in_blks[block].add(number)
                        in_rows[row].add(number)
                    if len(can_cols)==1:
                        found_one_col = True
                        col = can_cols[0]
                        in_blks[block].add(number)
                        in_cols[col].add(number)
            if not found_one_row and not found_one_col:
                break
    return None,None,None

def findSureSquareByRow():
    """
    排除法2：对于每一个数字，在每一行上看看它是否只有一个可填位置
    """
    for number in range(1, 10):
        for row in range(1,10):
            if number not in rows[row]:
                can_cols = []
                for j in range(1,10):
                    block = which_block(row,j)
                    if number not in cols[j] and number not in blks[block] and board[row][j]==0:
                        can_cols.append(j)
                if len(can_cols)==1: #只能填在row行某列上
                    col=can_cols[0]
                    return number,row,col
    return None, None, None

def findSureSquareByCol():
    """
    排除法3：对于每一个数字，在每一列上看看它是否只有一个可填位置
    """
    for number in range(1, 10):
        for col in range(1, 10):
            if number not in cols[col]:
                can_rows = []
                for i in range(1, 10):
                    block = which_block(i, col)
                    if number not in rows[i] and number not in blks[block] and board[i][col]==0:
                        can_rows.append(i)
                if len(can_rows) == 1: #只能填在某行col列上
                    row=can_rows[0]
                    return number,row,col
    return None,None,None

def solve(unsolved):
    if unsolved == 0:
        return True

    # 显示用
    delay_fps(SPEED)

    number,row,col=findSureSquareByBlock()
    if number is not None:
        # set_fill_color("white")
        # fill_rect(500,10,800,80)
        # draw_text(500, 40, f"规则1 {row},{col}只能填{number} {board[row][col]}")
        # pause()
        fill(row, col, number)
        draw_number_at(row, col, number, Color.BLACK)
        if solve(unsolved - 1):
            return True
        unfill(row, col)
        draw_number_at(row, col, 0, Color.BLACK)
        return False

    number,row,col=findSureSquareByRow()
    if number is not None:
        # set_fill_color("white")
        # fill_rect(500,10,800,80)
        # draw_text(500, 40, f"规则2: {row},{col}只能填{number} {board[row][col]}")
        # pause()
        fill(row, col, number)
        draw_number_at(row, col, number, Color.BLACK)
        if solve(unsolved - 1):
            return True
        unfill(row, col)
        draw_number_at(row, col, 0, Color.BLACK)
        return False

    number,row,col=findSureSquareByCol()
    if number is not None:
        # set_fill_color("white")
        # fill_rect(500,10,800,80)
        # draw_text(500, 40, f"规则3: {row},{col}只能填{number} {board[row][col]}")
        # pause()
        fill(row, col, number)
        draw_number_at(row, col, number, Color.BLACK)
        if solve(unsolved - 1):
            return True
        unfill(row, col)
        draw_number_at(row, col, 0, Color.BLACK)
        return False

    # 找出可填的数字数量最少的格子
    possibles,c = findMinPossibles1()

    # 尝试填写该格子
    if len(c.possibles)!=1:
    #     fill_rect(500,10,800,80)
    #     draw_text(500, 40, f"规则4 {c.x},{c.y}只能填{c.possibles}")
    #     pause()
    # else:
        possibles,c = findMinPossibles2(possibles,c)

        # # 尝试填写该格子
        # if len(c.possibles)==1:
        #     fill_rect(500,10,800,80)
        #     draw_text(500, 40, f"规则5 {c.x},{c.y}只能填{c.possibles}")
        #     pause()
        # else:
        #     fill_rect(500, 10, 800, 80)
        #     draw_text(500, 40, f"{c.x},{c.y}只能填{c.possibles}")
        #     pause()

    if len(c.possibles) > 1:
        fill_rect(500, 10, 800, 80)
        draw_text(500, 40, f"{c.x},{c.y}只能填{c.possibles}")
        pause()

    for v in c.possibles:
        fill(c.x, c.y, v)
        draw_number_at(c.x, c.y, v, Color.BLACK)
        if solve(unsolved - 1):
            return True
        unfill(c.x, c.y)
        draw_number_at(c.x, c.y, 0, Color.BLACK)

    return False


def findMinPossibles1():
    """
    找到能填的数字最少的格子
    :return:
    """
    c = CandiateSquare()
    min_possible_count = 10
    possibles = [[None for i in range(10)] for j in range(10)]
    for i in range(1, 10):
        for j in range(1, 10):
            if board[i][j] == 0:
                possibles[i][j] = calculatePossible(i, j)
                if len(possibles[i][j]) < min_possible_count:
                    min_possible_count = len(possibles[i][j])
                    c.x = i
                    c.y = j
                    c.possibles = possibles[i][j]
                    if len(c.possibles)<2:
                        return None,c
    return possibles,c

def findMinPossibles2(possibles,c):
    """
    当同一行或者同一列有两个格同时只能填同样的两个数时，同一行/列上的其他格必然不能填这两个数
    :param possibles:
    :param c:
    :return:
    """
    if len(c.possibles)==2:

        while True:
            found = False
            row = c.x
            col = c.y
            for i in range(10):
                if i!=col and possibles[row][col] == possibles[row][i]:
                    for j in range(10):
                        if j !=i and j!=col and possibles[row][j] is not None:
                            possibles[row][j].difference_update(possibles[row][i])
                            found = True
                            if len(possibles[row][j])<2:
                                c.x=row
                                c.y=j
                                c.possibles = possibles[row][j]
                            return possibles,c
            if not found:
                break

    return possibles,c


def main():
    init()
    load_board(DATA_FILE)
    draw_board()
    draw_rect_text(10, 550, 700, 50, "按任意键开始...")
    pause()
    fill_rect(10, 550, 710, 600)
    draw_rect_text(10, 550, 700, 50, "正在穷举...")

    # 将数独中已有的数字做标记
    for i in range(1, 10):
        for j in range(1, 10):
            if board[i][j] != 0:
                tag(i, j, board[i][j])

    #初始化所有未填格的possible
    for i in range(1,10):
        for j in range(1,10):
            if board[i][j] == 0:
                tag(i, j, board[i][j])

    solve(count_unsolved())
    fill_rect(10, 550, 710, 600)
    draw_rect_text(10, 550, 700, 50, "找到答案了！按任意键退出...")
    pause()
    close_graph()

easy_run(main)