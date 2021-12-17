import json
import random
def isIn(spot, board):
    return not (spot[0] < 0 or spot[0] >= len(board) or spot[1] < 0 or spot[1] >= len(board[0]))
def isOpenOrControlled(spot, board):
    return board[spot[0]][spot[1]] in [0,-1]
def weightMove(board,i,j):
    weight = 0
    for rdelt in [-1,0,1]:
        for cdelt in [-1,0,1]:
            multiplex = 0
            curspot = (i + multiplex*rdelt,j + multiplex*cdelt)
            while(isIn(curspot, board) and isOpenOrControlled(curspot, board) and multiplex <= 3):
                # print(isIn(curspot, board))
                # print(isOpenOrControlled(curspot, board))
                # print(curspot)
                multiplex += 1
                curspot = (i + multiplex*rdelt,j + multiplex*cdelt)
                if multiplex == 3:
                    weight += 1
    return weight - 1
def translate(n):
    if n==1:
        return "A"
    if n==-1:
        return "B"
    return "X"
def pB(board):
    print("| ",0, " ",1, " ",2, " ",3, " ",4, " ",5, " ",6," |")
    for row in board:
        print("| ",translate(row[0]), " ", translate(row[1]), " ", translate(row[2]), " ",  translate(row[3]), " ",  translate(row[4]), " ",  translate(row[5]), " ",  translate(row[6])," |")
    print()
def isN(board,r,c,n,direction=None):
    found = False
    # print(r,c,direction,n)
    if n == 1:
        return True
    if direction is None:
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                if (i!=0 or j!=0) and r+i<6 and r+i >=0 and c+j>=0 and c+j<7 and board[r][c] == board[r+i][c+j] and not found:
                    found = isN(board,r+i,c+j,n-1,(i,j)) or isN(board,r+i,c+j,n,(-i,-j))
    else:
        if r+direction[0] >= 0 and r+direction[0] < 6 and c+direction[1] >=0 and c+direction[1] < 7 and board[r][c] == board[r+direction[0]][c+direction[1]]:
            found = isN(board,r+direction[0],c+direction[1],n-1,direction)
    return found
def hasWon(board,player=[1,-1]):
    hasWon = False
    for i in range(6):
        for j in range(7):
            if board[i][j] != 0 and board[i][j] in player and isN(board,i,j,4):
                hasWon = True
                break
    return hasWon
def copy(board):
    out = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
    for i in range(6):
        for j in range(7):
            out[i][j] = board[i][j]
    return out
def copyC(nextInC):
    out = [0,0,0,0,0,0,0]
    for i in range(7):
        out[i] = nextInC[i]
    return out
def move(board,r,c,player):
    board[r][c] = player
    return (r,c)
def isFull(nextInC):
    isFull = True
    for n in nextInC:
        if n >= 0:
            isFull = False
    return isFull
def letWin(board,nextInC,i):
    temp_board = copy(board)
    c_nextInC = copyC(nextInC)
    temp_board[c_nextInC[i]][i] == -1
    c_nextInC[i] -= 1
    canWin = False
    for i in [3,4,2,5,1,6,0]:
            if nextInC[i] < 0:
                continue
            temp_board[c_nextInC[i]][i] = 1
            if hasWon(temp_board,[1]):
                canWin = True
                temp_board[c_nextInC[i]][i] = 0
                break
            temp_board[c_nextInC[i]][i] = 0
    return canWin
def loadStates():
    with open('C:\\Users\\LOWRYEC17\\reinforcement-learning-connect-four-ai\\src\\states.json','r') as json_file:
        states = json.load(json_file)
    return states

def writeStates(states):
    with open('C:\\Users\\LOWRYEC17\\reinforcement-learning-connect-four-ai\\src\\states.json','w') as outfile:
        json.dump(states, outfile)

def stateKeyOf(board):
    out = ""
    for row in board:
        for n in row:
            out += str(n)
    return out

states = loadStates()
wins = 0
ties = 0
N = 600000
for t in range(N):
    alpha = 0.008
    board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
    # pB(board)
    # print(isN(board,0,0,4))
    nextInC = [5,5,5,5,5,5,5]
    # print(hasWon(board))
    finished = False
    aiFirst = True
    winner = 0
    # answer = input("Would you like to go first? (y/n)")
    preboardState = None
    answer = random.choice(['y','n'])
    if answer == "y":
        aiFirst = False
    while(not finished):
        if aiFirst:
            # moved = False
            preboardState = stateKeyOf(board)
            currStateVal = states.get(stateKeyOf(board))
            if not currStateVal:
                currStateVal = 0.5
                alpha = 0.04
                states[stateKeyOf(board)] = 0.5
            else:
                alpha = 0.008
            
            if random.choice([0,0,0,0,1]) == 0:
                best_spot = (5,3)
                best_weight = 0
                temp_board = copy(board)
                for j in range(7):
                    i = nextInC[j]
                    if temp_board[i][j] != 0:
                        continue
                    temp_board[i][j] = 1
                    currVal = states.get(stateKeyOf(temp_board),0.5)
                    if currVal > best_weight:
                        best_weight = currVal
                        best_spot = (i,j)
                    elif currVal == best_weight:
                        if random.choice([0,1]) == 1:
                            best_weight = currVal
                            best_spot = (i,j)
                    temp_board[i][j] = 0
                move(board, best_spot[0],best_spot[1],1)
                nextInC[best_spot[1]] -= 1
            # moved = True

            else:
                moved = False
                while(not moved):
                    col = random.choice([0,1,2,3,4,5,6])
                    row = nextInC[col]
                    if board[row][col] == 0:
                        move(board,row,col,1)
                        nextInC[col] -= 1
                        moved = True

            if hasWon(board,[1]):
                    finished = True
                    winner = 1
                    states[stateKeyOf(board)] = 1
            if not states.get(stateKeyOf(board)):
                states[stateKeyOf(board)] = 0.5
                alpha = 0.04
            else:
                alpha = 0.008

            states[preboardState] = states.get(preboardState) + alpha*(states.get(stateKeyOf(board)) - states.get(preboardState))
            preboardState = stateKeyOf(board)

            # pB(board)
        if isFull(nextInC):
            finished = True
            break
            
        if not aiFirst:
            aiFirst = True

        if finished:
            break

        ##############################################################

        # hasMoved = False
        # while(not hasMoved):
        #     col = int(input("Where do you want to move? ('column 0-6')"))
        #     pMove = (nextInC[col],col)
        #     if len(pMove) < 2 or int(pMove[0]) not in [0,1,2,3,4,5] or int(pMove[1]) not in [0,1,2,3,4,5,6] or board[int(pMove[0])][int(pMove[1])] != 0:
        #         print("Invalid entry...try again")
        #     else:
        #         move(board,int(pMove[0]),int(pMove[1]),-1)
        #         hasMoved = True
        #         nextInC[col] -= 1
        #         if hasWon(board,[-1]):
        #             finished = True
        #             winner = -1
        #             states[stateKeyOf(board)] = 0

        ###############################################################

        # have move to connect four, do it
        if random.choice([0,0,0,0,1]) == 0:
            moved = False
            columns = random.sample([0,1,2,3,4,5,6],7)
            temp_board = copy(board)
            for i in columns:
                if nextInC[i] < 0:
                    continue
                temp_board[nextInC[i]][i] = -1
                if hasWon(temp_board,[-1]):
                    move(board,nextInC[i],i,-1)
                    nextInC[i] -= 1
                    # print("1")
                    moved = True
                    finished = True
                    states[stateKeyOf(board)] = 0
                    winner = -1
                    break
                temp_board[nextInC[i]][i] = 0
            # o has move to connect four, take it
            if not moved:
                for i in columns:
                    if nextInC[i] < 0:
                        continue
                    temp_board[nextInC[i]][i] = 1
                    if hasWon(temp_board,[1]):
                        move(board,nextInC[i],i,-1)
                        nextInC[i] -= 1
                        # print("2")
                        moved = True
                        break
                    temp_board[nextInC[i]][i] = 0
            # otherwise, have move connect three, do it
            if not moved:
                for i in columns:
                    if nextInC[i] < 0:
                        continue
                    temp_board[nextInC[i]][i] = -1
                    if isN(temp_board,nextInC[i],i,3) and not letWin(board,nextInC,i):
                        move(board,nextInC[i],i,-1)
                        nextInC[i] -= 1
                        # print("3")
                        moved = True
                        break
                    temp_board[nextInC[i]][i] = 0
            # otherwise, if o has move connect three, take it
            if not moved:
                for i in columns:
                    if nextInC[i] < 0:
                        continue
                    temp_board[nextInC[i]][i] = 1
                    if isN(temp_board,nextInC[i],i,3) and not letWin(board,nextInC,i):
                        move(board,nextInC[i],i,-1)
                        nextInC[i] -= 1
                        # print("4")
                        moved = True
                        break
                    temp_board[nextInC[i]][i] = 0
            # otherwise, have move connect two, do it
            if not moved:
                for i in columns:
                    if nextInC[i] < 0:
                        continue
                    temp_board[nextInC[i]][i] = -1
                    if isN(temp_board,nextInC[i],i,2) and not letWin(board,nextInC,i):
                        move(board,nextInC[i],i,-1)
                        nextInC[i] -= 1
                        # print("5")
                        moved = True
                        break
                    temp_board[nextInC[i]][i] = 0
            # otherwise, if o has move connect two, take it
            if not moved:
                for i in columns:
                    if nextInC[i] < 0:
                        continue
                    temp_board[nextInC[i]][i] = 1
                    if isN(temp_board,nextInC[i],i,2) and not letWin(board,nextInC,i):
                        move(board,nextInC[i],i,-1)
                        nextInC[i] -= 1
                        moved = True
                        # print("6")
                        break
                    temp_board[nextInC[i]][i] = 0
            # otherwise, middle
            if isFull(nextInC):
                finished = True
                break
            if not moved:
                # print("7")
                move(board,nextInC[3],3,-1)
                nextInC[3] -= 1
                moved = True
            if not moved:
                print("Something went wrong...no good moves")
        else:
            moved = False
            while(not moved):
                    col = random.choice([0,1,2,3,4,5,6])
                    row = nextInC[col]
                    if board[row][col] == 0:
                        move(board,row,col,-1)
                        nextInC[col] -= 1
                        moved = True

        ##############################################################################

        # ###
        # moved = False
        #     # have move to connect four, do it
        # temp_board = copy(board)
        # for i in [3,4,2,5,1,6,0]:
        #         if nextInC[i] < 0:
        #             continue
        #         temp_board[nextInC[i]][i] = -1
        #         if hasWon(temp_board,[-1]):
        #             move(board,nextInC[i],i,-1)
        #             nextInC[i] -= 1
        #             # print("1")
        #             moved = True
        #             finished = True
        #             winner = -1
        #             break
        #         temp_board[nextInC[i]][i] = 0
        #     # o has move to connect four, take it
        # if not moved:
        #         for i in [3,4,2,5,1,6,0]:
        #             if nextInC[i] < 0:
        #                 continue
        #             temp_board[nextInC[i]][i] = 1
        #             if hasWon(temp_board,[1]):
        #                 move(board,nextInC[i],i,-1)
        #                 nextInC[i] -= 1
        #                 # print("2")
        #                 moved = True
        #                 break
        #             temp_board[nextInC[i]][i] = 0
            
        # if not moved:
        #         best_spot = (3,3)
        #         best_weight = -1
        #         for j in range(7):
        #             i = nextInC[j]
        #             currWeight = weightMove(board,i,j)
        #             if currWeight > best_weight:
        #                 best_weight = currWeight
        #                 best_spot = (i,j)
        #         move(board, best_spot[0],best_spot[1],-1)
        #         nextInC[best_spot[1]] -= 1
        #         moved = True
                ###
        if hasWon(board,[-1]):
            states[stateKeyOf(board)] = 0
            winner = -1
            finished = True
        if isFull(nextInC):
                finished = True
                break
        # pB(board)
        if states.get(stateKeyOf(board)) is None:
                states[stateKeyOf(board)] = 0.5
                alpha = 0.04
        else:
                alpha = 0.008
        if preboardState and states.get(preboardState) is not None:
            states[preboardState] = states.get(preboardState) + alpha*(states.get(stateKeyOf(board)) - states.get(preboardState))
        # print(preboardState)
        # print(states)

    # if winner == 1:
    #     print("AI wins")
    # elif winner == -1:
    #     print('You win')
    # else:
    #     print("It's a draw")

    if winner == 1:
        wins +=1
    if winner == 0:
        ties += 1
    if (t%100) == 0:
        print(t)
print("Wins:",wins/N)
print("Ties:",ties/N)
print("Losses:",(N-wins-ties)/N)
print(len(states))
writeStates(states)