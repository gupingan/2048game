import random
import json


class Model:
    def __init__(self):
        self.grid_size = 4
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.last_move_direction = None
        self.score = 0
        self.highest_score = 0
        self.load_highest_score()

    def add_random_number(self):
        print("add_random_number 被调用")
        # Select a random empty cell
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            # Assign either 2 or 4 to the cell with a 0.9/0.1 probability ratio
            self.grid[i][j] = random.choices([2, 4], weights=(0.9, 0.1))[0]

    def reset(self):
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.add_random_number()
        self.add_random_number()

    def move_left(self):
        for row in self.grid:
            # 合并相邻的相同数字
            for i in range(self.grid_size - 1):
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    row[i + 1] = 0
                    self.score += row[i]
            # 移动数字
            for i in range(self.grid_size):
                if row[i] == 0:
                    for j in range(i + 1, self.grid_size):
                        if row[j] != 0:
                            row[i], row[j] = row[j], row[i]
                            break
        self.add_random_number()
        if self.score > self.highest_score:
            self.highest_score = self.score
        self.last_move_direction = "left"

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
        data = {'highest_score': self.highest_score}
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_highest_score(self, filename="./2048_set.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.highest_score = data['highest_score']
        except FileNotFoundError:
            # 如果文件不存在，就不做任何处理
            pass

    def check_win(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 2048:
                    return True
        return False

    def check_lost(self):
        # Check if there are any empty cells or adjacent cells with the same value
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False
                if j < self.grid_size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < self.grid_size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True


if __name__ == '__main__':
    model = Model()
    print(model.grid)
    model.move_left()
    print(model.grid)
