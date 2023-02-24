# This code is paritaly based on the followwing github public repo
# https://github.com/LeanMilk/Flood-It

from copy import deepcopy
import random
import time


class Player:

    def __init__(self):
        pass


class PlayerRandom(Player):

    def __init__(self):
        super().__init__()

    def findMove(self, board):
        children = board.children()

        return random.choice(children)[1]


class PlayerH3(Player):
    def __init__(self):
        super().__init__()

    def findMove(self, board):
        children = list(sorted(board.children(), key=lambda x: x[0].H3_score()))

        return children[0][1]

class PlayerH1(Player):
    def __init__(self):
        super().__init__()

    def findMove(self, board):
        children = list(sorted(board.children(), key=lambda x: x[0].H1_score(),reverse=True))

        return children[0][1]

class PlayerH4(Player):
    def __init__(self):
        super().__init__()

    def findMove(self, board):
        children = list(sorted(board.children(), key=lambda x: x[0].H4_score(),reverse=True))
        return children[0][1]

class PlayerH2(Player):
    def __init__(self):
        super().__init__()

    def findMove(self, board):
        children = list(sorted(board.children(), key=lambda x: x[0].H2_score(),reverse=True))
        return children[0][1]

if __name__ == '__main__':
    from board import Board
    import copy
    
    simulations = True
    oneTime = False
    UCS = True
    numberOfBoards = 3
    boardSize = 6
    numberOfColors = 3
            

    if simulations: 
        
        RandomTime = H1Time = H2Time = H3Time = H4Time = UCS_time = 0
        RandomSteps = H1Steps = H2Steps = H3Steps = H4Steps = UCS_steps = 0
        for c in range(numberOfBoards):
            print('Board',c+1,'out of', numberOfBoards)
            b = Board(size=boardSize, color=numberOfColors)
            b1 = deepcopy(b)
            b2 = deepcopy(b)
            b3 = deepcopy(b)
            b4 = deepcopy(b)
            b5 = deepcopy(b)

            # random
            start_time = time.time()
            p = PlayerRandom()
            i = 0
            while not b.isOver():
                    i += 1
                    m = p.findMove(b)
                    b.move(m)
            RandomTime += time.time() - start_time
            RandomSteps += i

            # H1
            start_time = time.time()
            p = PlayerH1()
            i = 0
            while not b1.isOver():
                    i += 1
                    m = p.findMove(b1)
                    b1.move(m)
            H1Time += time.time() - start_time
            H1Steps += i

            # H2
            start_time = time.time()
            p = PlayerH2()
            i = 0
            while not b2.isOver():
                    i += 1
                    m = p.findMove(b2)
                    b2.move(m)
            H2Time += time.time() - start_time
            H2Steps += i

            # H3
            start_time = time.time()
            p = PlayerH3()
            i = 0
            while not b3.isOver():
                    i += 1
                    m = p.findMove(b3)
                    b3.move(m)
            H3Time += time.time() - start_time
            H3Steps += i

            # H4
            start_time = time.time()
            p = PlayerH4()
            i = 0
            while not b4.isOver():
                    i += 1
                    m = p.findMove(b4)
                    b4.move(m)
            H4Time += time.time() - start_time
            H4Steps += i

            # UCS
            if not UCS:
                continue
            start_time = time.time()
            stack = [b5]
            while len(stack) != 0:
                stack.sort(reverse=True)
                x = stack.pop()
                if x.isOver():
                    UCS_steps += x.steps
                    break
                children = x.children()
                n = len(children)
                for i in range(n):
                    stack.append(children[i][0])
            UCS_time += time.time() - start_time

        print('Results ----------------------------------')
        print('Number of boards:', numberOfBoards)
        print('Size of the board:', boardSize)
        print('Number of colors:', numberOfColors)
        print('------------------------------------------')
        print('Random:' ,'Time in seconds:',int(RandomTime),", Average steps: ", RandomSteps / numberOfBoards)
        print('H1:' ,'Time in seconds:', int(H1Time),", Average steps: ", H1Steps / numberOfBoards)
        print('H2:' ,'Time in seconds:', int(H2Time),", Average steps: ", H2Steps / numberOfBoards)
        print('H3:' ,'Time in seconds:',int(H3Time),", Average steps: ", H3Steps / numberOfBoards)
        print('H4:' ,'Time in seconds:',int(H4Time), ", Average steps: ", H4Steps / numberOfBoards)
        if UCS:
            print('UCS:' ,'Time in seconds:',int(UCS_time), ", Average steps: ",UCS_steps / numberOfBoards)


    if oneTime:
        
        algorithm = 'h2'
        i = 0
        b = Board(size=boardSize, color=numberOfColors)
        b.print()
        if algorithm.upper() == "RAND":
            p = PlayerRandom()
            while not b.isOver():
                i += 1
                print(i)
                m = p.findMove(b)
                print(m)
                b.move(m)
                b.print()
        elif algorithm.upper() == "H1":
            p = PlayerH1()
            while not b.isOver():
                i += 1
                print(i)
                m = p.findMove(b)
                print(m)
                b.move(m)
                b.print()
        elif algorithm.upper() == "H3":
            p = PlayerH3()
            while not b.isOver():
                i += 1
                print(i)
                m = p.findMove(b)
                print(m)
                b.move(m)
                b.print()
        elif algorithm.upper() == "H4":
            p = PlayerH4()
            while not b.isOver():
                i += 1
                print(i)
                m = p.findMove(b)
                print(m)
                b.move(m)
                b.print()
        elif algorithm.upper() == "H2":
            p = PlayerH2()
            while not b.isOver():
                i += 1
                print(i)
                m = p.findMove(b)
                print(m)
                b.move(m)
                b.print()
        else:
            print("ERROR: Not a valid algorithm")
