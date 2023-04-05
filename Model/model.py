"""
model.py
==========

这个Model类是2048游戏的核心类
实现了2048游戏的逻辑，包括移动、得分、最高得分、存储和读取最高得分、检查胜利和失败等功能。

- add_random_number方法是在随机位置添加数字
- reset方法是重置游戏状态
- move_left、move_right、move_up和move_down方法是移动网格并在适当的时候合并数字
- check_win方法用于检查是否赢得游戏，check_lost方法用于检查是否输掉游戏

Author: 顾初见（Ronan Gu） <ronangu@foxmail.com>

Date: 2023-4-5
"""
import random
import json


class Model:
    def __init__(self):
        self.grid_size = 4  # 网格的大小为4x4
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]  # 初始化网格
        self.last_move_direction = None  # 上一次的移动方向
        self.score = 0  # 当前得分
        self.highest_score = 0  # 最高得分
        self.load_highest_score()  # 加载最高得分

    def add_random_number(self):
        """
        随机在网格上添加一个数字
        :return:
        """
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choices([2, 4], weights=(0.9, 0.1))[0]

    def reset(self):
        """
        重置游戏状态
        :return:
        """
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.add_random_number()
        self.add_random_number()

    def move_left(self):
        """
        向左移动
        :return:
        """
        for row in self.grid:
            last_non_zero = -1
            for i in range(self.grid_size):
                # 将非零数字向左移动
                if row[i] != 0:
                    if i != last_non_zero + 1:
                        row[last_non_zero + 1] = row[i]
                        row[i] = 0
                    last_non_zero += 1
            # 合并相邻的相同数字
            i = 0
            while i < last_non_zero:
                if row[i] == row[i + 1]:
                    row[i], row[i + 1] = row[i] * 2, 0
                    self.score += row[i]
                    i += 2
                else:
                    i += 1
            # 再将非零数字向左移动
            last_non_zero = -1
            for i in range(self.grid_size):
                if row[i] != 0:
                    if i != last_non_zero + 1:
                        row[last_non_zero + 1] = row[i]
                        row[i] = 0
                    last_non_zero += 1
        # 添加一个随机数字
        self.add_random_number()
        # 检查并更新最高得分
        if self.score > self.highest_score:
            self.highest_score = self.score
        self.last_move_direction = "left"  # 更新上一次的移动方向，本来用于view层更新动画的

    def move_right(self):
        # 先翻转再移动再翻转回来
        self.grid = [row[::-1] for row in self.grid]
        self.move_left()
        self.grid = [row[::-1] for row in self.grid]
        self.last_move_direction = "right"

    def move_up(self):
        # 先转置再移动再转置回来
        self.grid = [list(x) for x in zip(*self.grid)]
        self.move_left()
        self.grid = [list(x) for x in zip(*self.grid)]
        self.last_move_direction = "up"

    def move_down(self):
        # 先转置再翻转再移动再翻转再转置回来
        self.grid = [list(x) for x in zip(*self.grid[::-1])]
        self.move_left()
        self.grid = [list(x) for x in zip(*self.grid)][::-1]
        self.last_move_direction = "down"

    def save_highest_score(self, filename="./2048_set.json"):
        """
        将最高分进行存储
        :param filename:默认路径./2048_set.json"
        :return:
        """
        data = {'highest_score': self.highest_score}
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_highest_score(self, filename="./2048_set.json"):
        """
        从文件中读取之前最高分数
        :param filename:默认路径./2048_set.json"
        :return:
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.highest_score = data['highest_score']
        except FileNotFoundError:
            pass

    def check_win(self):
        """
        检查是否有任何一个格子的数字等于2048
        :return:
        """
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 2048:
                    return True
        return False

    def check_lost(self):
        """
        检查是否有任何一个格子为空或者相邻的格子有相同的数字
        :return:
        """
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False
                if j < self.grid_size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < self.grid_size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True


# 代码测试部分
if __name__ == '__main__':
    model = Model()
    print(model.grid)
    model.move_left()
    print(model.grid)
