# This code is paritaly based on the followwing github public repo
# https://github.com/LeanMilk/Flood-It

import random
import string
import copy
from termcolor import colored

dict_colors = {
        "A": "red",
        "B": 'yellow',
        "C": 'green',
        "D": 'blue',
        "E": 'cyan',
        "F": 'magenta',
        "G": 'white',
        "H": 'grey'
    }

class Board(object):
    COLORS = string.ascii_uppercase


    def __init__(self, orig=None, size=10, color=4,s = 0):

        self.COLORS = self.COLORS[0:color] 
        self.size = size
        self.board = [[' ' for i in range(self.size)] for i in range(self.size)]
        self.FC = 0
        self.FLOODED = []
        self.GROUPS = []
        self.Borders = []
        self.steps = 0
        self.reset()

        if orig:
            self.COLORS = copy.deepcopy(orig.COLORS)
            self.size = orig.size
            self.board = copy.deepcopy([list(col) for col in orig.board])
            self.FC = copy.deepcopy(orig.FC)
            self.FLOODED = copy.deepcopy(orig.FLOODED)
            self.GROUPS = copy.deepcopy(orig.GROUPS)
        self.steps += s
    def __lt__(self, obj):
        return self.steps < obj.steps

    def reset(self):
        for i in range(self.size):
            for j in range(self.size):
                # get a random color
                tempc = self.COLORS[random.randrange(len(self.COLORS))]

                # set the color for this block
                self.board[i][j] = tempc
                self.GROUPS.append([tempc, [(i, j)]])

        # grouping
        while True:
            done = True
            for n, g in enumerate(self.GROUPS):
                for coor in g[1]:
                    x, y = coor
                    for m, gg in enumerate(self.GROUPS):
                        if n != m and g[0] == gg[0]:
                            if (y > 0 and (x, y - 1) in gg[1]) or (x > 0 and (x - 1, y) in gg[1]):
                                if n < m:
                                    tempg = g
                                    tempg[1] = tempg[1] + gg[1]
                                    keep = n
                                    dele = gg
                                if n > m:
                                    tempg = gg
                                    tempg[1] = tempg[1] + g[1]
                                    keep = m
                                    dele = g
                                done = False
                                break
                    if not done:
                        break
                if not done:
                    break
            if done:
                break
            else:
                self.GROUPS[keep] = tempg
                self.GROUPS.remove(dele)

        self.FC = self.GROUPS[0][0]
        self.FLOODED = self.GROUPS[0][1]
        del self.GROUPS[0]

    # ---------------------------------------------

    def hash(self):
        output = ""
        for g in self.GROUPS:
            output += g[0] + str(g[1][0])
        return output

    # ---------------------------------------------

    def move(self, c):
        self.FC = c
        for coor in self.FLOODED:
            x, y = coor
            self.board[x][y] = c
        self.flood()

    # ---------------------------------------------

    def children(self):
        children = []
        for c in self.COLORS:
            if c != self.FC:
                child = Board(orig=self,s=self.steps + 1)
                child.move(c)
                if len(child.GROUPS) < len(self.GROUPS):
                    children.append((child, c))
        return children

    # ---------------------------------------------

    def isOver(self):
        if len(self.GROUPS) == 0:
            return True
        else:
            return False

    # ---------------------------------------------

    def H3_score(self):
        return len(self.GROUPS) / len(self.COLORS)

    def H1_score(self):
        return len(self.FLOODED)

    def H4_score(self):
        d = 0
        for f in self.FLOODED:
            x = f[0] + f[1]
            if x > d:
                d = x
        return d
    
    def H2_score(self):
        d = 0 
        for f in self.FLOODED:
            x,y = f[0],f[1]
            if x - 1 > 0:
                if self.board[x-1][y] != self.FC:
                    d += 1
                    continue
            if x + 1 < self.size:
                if self.board[x+1][y] != self.FC:
                    d += 1
                    continue
            if y - 1 > 0:
                if self.board[x][y-1] != self.FC:
                    d += 1
                    continue
            if y + 1 < self.size:
                if self.board[x][y+1] != self.FC:
                    d += 1
                    continue

        return d

    # ---------------------------------------------

    # merge adjacent same color groups in larger group and update self.GROUPS
    # continues to check until no update is made, then break the loop. 
    def flood(self):

        while True:
            done = True
            for coor in self.FLOODED:
                x, y = coor
                for n, g in enumerate(self.GROUPS):
                    if self.FC == g[0]:
                        if (y < self.size and (x, y + 1) in g[1]) or (x <= self.size and (x + 1, y) in g[1]):
                            tempg = g[1]  
                            done = False
                            break
                if not done:
                    break
            if done:
                break
            else:
                self.FLOODED += tempg 
                self.Borders += tempg
                del self.GROUPS[n]

    # ---------------------------------------------

    def print(self):
        print()
        print('+' + '---+' * self.size)
        for i in range(self.size):
            row = '|'
            for j in range(self.size):
                row += ' ' + str(colored(self.board[i][j], dict_colors[self.board[i][j]])) + ' |'
            print(row)
            print('+' + '---+' * self.size)
        print()

    def show(self):
        print(self.FC)
        print(self.FLOODED)
        print(len(self.GROUPS))
        print(self.GROUPS)


if __name__ == "__main__":

    b = Board(size=5, color=3)
    b.print()
    i = 0
    while not b.isOver():
        inp = input("Input the color: ")
        if inp.upper() in b.COLORS:
            b.move(inp.upper())
            i += 1
            print("Moves: " + str(i))
            b.print()
        else:
            print("Invalid input. ")

    print('You have completed the game')
