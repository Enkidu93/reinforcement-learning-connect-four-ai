#
#
#
#
#
# _ _ _ _ _ _ _
def translate(n):
    if n==1:
        return "A"
    if n==-1:
        return "B"
    return "X"
# def pB(board):
#     print("|\t",0, "\t",1, "\t",2, "\t",3, "\t",4, "\t",5, "\t",6,"\t|")
#     for row in board:
#         print("|\t",translate(row[0]), "\t", translate(row[1]), "\t", translate(row[2]), "\t",  translate(row[3]), "\t",  translate(row[4]), "\t",  translate(row[5]), "\t",  translate(row[6]),"\t|")
#     print()
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

# def createsTriple(board,numTriples,player=[1,-1]):
#     newNumTriples = 0
#     for i in range(6):
#         for j in range(7):
#             if board[i][j] != 0 and board[i][j] in player and isN(board,i,j,4):
#                 pass

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
    temp_board[c_nextInC[i]][i] == 1
    c_nextInC[i] -= 1
    canWin = False
    for i in [3,4,2,5,1,6,0]:
            if nextInC[i] < 0:
                continue
            temp_board[c_nextInC[i]][i] = -1
            if hasWon(temp_board,[-1]):
                canWin = True
            temp_board[c_nextInC[i]][i] = 0
    return canWin


board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
pB(board)
# print(isN(board,0,0,4))
nextInC = [5,5,5,5,5,5,5]
# print(hasWon(board))
finished = False
aiFirst = True
winner = 0
answer = input("Would you like to go first? (y/n)")
if answer == "y":
    aiFirst = False
while(not finished):
    if aiFirst:
        moved = False
        # have move to connect four, do it
        temp_board = copy(board)
        for i in [3,4,2,5,1,6,0]:
            if nextInC[i] < 0:
                continue
            temp_board[nextInC[i]][i] = 1
            if hasWon(temp_board,[1]):
                move(board,nextInC[i],i,1)
                nextInC[i] -= 1
                # print("1")
                moved = True
                finished = True
                winner = 1
                break
            temp_board[nextInC[i]][i] = 0
        # o has move to connect four, take it
        if not moved:
            for i in [3,4,2,5,1,6,0]:
                if nextInC[i] < 0:
                    continue
                temp_board[nextInC[i]][i] = -1
                if hasWon(temp_board,[-1]):
                    move(board,nextInC[i],i,1)
                    nextInC[i] -= 1
                    # print("2")
                    moved = True
                    break
                temp_board[nextInC[i]][i] = 0
        # otherwise, have move connect three, do it
        if not moved:
            for i in [3,4,2,5,1,6,0]:
                if nextInC[i] < 0:
                    continue
                temp_board[nextInC[i]][i] = 1
                if isN(temp_board,nextInC[i],i,3) and not letWin(board,nextInC,i):
                    move(board,nextInC[i],i,1)
                    nextInC[i] -= 1
                    # print("3")
                    moved = True
                    break
                temp_board[nextInC[i]][i] = 0
        # otherwise, if o has move connect three, take it
        if not moved:
            for i in [3,4,2,5,1,6,0]:
                if nextInC[i] < 0:
                    continue
                temp_board[nextInC[i]][i] = -1
                if isN(temp_board,nextInC[i],i,3) and not letWin(board,nextInC,i):
                    move(board,nextInC[i],i,1)
                    nextInC[i] -= 1
                    # print("4")
                    moved = True
                    break
                temp_board[nextInC[i]][i] = 0
        # otherwise, have move connect two, do it
        if not moved:
            for i in [3,4,2,5,1,6,0]:
                if nextInC[i] < 0:
                    continue
                temp_board[nextInC[i]][i] = 1
                if isN(temp_board,nextInC[i],i,2) and not letWin(board,nextInC,i):
                    move(board,nextInC[i],i,1)
                    nextInC[i] -= 1
                    # print("5")
                    moved = True
                    break
                temp_board[nextInC[i]][i] = 0
        # otherwise, if o has move connect two, take it
        if not moved:
            for i in [3,4,2,5,1,6,0]:
                if nextInC[i] < 0:
                    continue
                temp_board[nextInC[i]][i] = -1
                if isN(temp_board,nextInC[i],i,2) and not letWin(board,nextInC,i):
                    move(board,nextInC[i],i,1)
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
            move(board,nextInC[3],3,1)
            nextInC[3] -= 1
            moved = True
        if not moved:
            print("Something went wrong...no good moves")
        pB(board)
        
    if not aiFirst:
        aiFirst = True

    if finished:
        break

    hasMoved = False
    while(not hasMoved):
        col = int(input("Where do you want to move? ('column 0-6')"))
        pMove = (nextInC[col],col)
        if len(pMove) < 2 or int(pMove[0]) not in [0,1,2,3,4,5] or int(pMove[1]) not in [0,1,2,3,4,5,6] or board[int(pMove[0])][int(pMove[1])] != 0:
            print("Invalid entry...try again")
        else:
            move(board,int(pMove[0]),int(pMove[1]),-1)
            hasMoved = True
            nextInC[col] -= 1
            if hasWon(board,[-1]):
                finished = True
                winner = -1
    if isFull(nextInC):
            finished = True
            break
    pB(board)

if winner == 1:
    print("AI wins")
elif winner == -1:
    print('You win')
else:
    print("It's a draw")
