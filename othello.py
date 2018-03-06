import turtle
from copy import copy, deepcopy

class Othello:
    def __init__(self):
        # create the board of 8x8 (initialize board to 0 to signify entire board is empty)
        self.board = [0] * 8
        for i in range(8):
            self.board[i] = [0] * 8
        # mark the initial start points on board
        self.board[3][4] = "w"
        self.board[4][3] = "w"
        self.board[3][3] = "b"
        self.board[4][4] = "b"
        # visualize the board
        self.drawboard()
    
    def drawboard(self):
        turtle.speed(0)
        turtle.tracer(0, 0)
        turtle.setworldcoordinates(-1, 9, 9, -1)
        i = 0
        j = 0
        k = 0
        turtle.penup()
        turtle.goto(0, 0)
        turtle.pendown()
        turtle.hideturtle()
        turtle.color('black', 'brown')
        # draw the board
        turtle.begin_fill()
        while i < 8:
            while j < 8:
                while k < 4:
                    turtle.forward(1)
                    turtle.left(90)
                    k += 1
                k = 0
                turtle.forward(1)
                j += 1
            turtle.backward(8)
            turtle.left(90)
            turtle.forward(1)
            turtle.right(90)
            j = 0
            i += 1
        turtle.end_fill()
        # number the columns
        colnum = 0
        while colnum < 8:
            turtle.penup()
            turtle.goto(-0.5, colnum + 0.5)
            turtle.pendown()
            turtle.write(colnum)
            colnum += 1
        # number the rows
        rownum = 0
        while rownum < 8:
            turtle.penup()
            turtle.goto(rownum + 0.5, -0.5)
            turtle.pendown()
            turtle.write(rownum)
            rownum += 1
        # mark intial start points on board
        turtle.penup()
        turtle.goto(3.5, 4.5)
        turtle.dot(50, 'white')
        turtle.goto(4.5, 3.5)
        turtle.dot(50, 'white')
        turtle.goto(3.5, 3.5)
        turtle.dot(50, 'black')
        turtle.goto(4.5, 4.5)
        turtle.dot(50, 'black')
        turtle.update()
    
    # this will be used as human player (human is black)
    def player1(self):
        turn = True
        m,n = self.getPossibleMoves(self.board, "b")
        if len(m) == 0:
            p1 = turtle.textinput("Othello", "No possible moves available, press any button to pass.")
            return False
        else:
            string = "Enter coordinates of next move:"
            while turn:
                p1 = tuple(int(x.strip()) for x in turtle.textinput("Othello", string).split(","))
                valid,flipped = self.isValidMove(self.board, p1[0], p1[1], "b")
                if valid != False:
                    # goto coordinates is flipped because goto takes input as (x,y)
                    turtle.goto(p1[1]+0.5, p1[0]+0.5)
                    turtle.dot(50, 'black')
                    self.board[p1[0]][p1[1]] = "b"
                    for i in valid:
                        turtle.goto(i[1]+0.5, i[0]+0.5)
                        turtle.dot(50, 'black')
                        self.board[i[0]][i[1]] = "b"
                    return
                else:
                    string = "Invalid move. Please reenter move."

    # this will be used as ai (ai is white)
    def player2(self):
        moves,flipped = self.getPossibleMoves(self.board, "w")
        # self.minimax(moves, flipped)
        # self.minimax_v2(moves, flipped)
        self.alphabeta(moves, flipped, -1, -1)

    def alphabeta(self, moves, flipped, minVal, maxVal):
        maxscore = 0
        maxmoves = []
        maxDepth = 2
        for i in moves:
            newBoard = self.getNewBoard(i[0], i[1], "w")
            newMoves, newflipped = self.getPossibleMoves(newBoard, "w")
            for move in newMoves:
                score = self.minPlay2(newBoard, moves, maxDepth-1, newflipped, minVal, maxVal)
                if score > maxscore: 
                    maxscore = score
                    maxmoves = move

        turtle.goto(maxmoves[1]+0.5, maxmoves[0]+0.5)
        turtle.dot(50, 'white')
        x,y = self.isValidMove(self.board, maxmoves[0], maxmoves[1], "w")
        
        for i in x:
            turtle.goto(i[1]+0.5, i[0]+0.5)
            turtle.dot(50, 'white')
            self.board[i[0]][i[1]] = "w"
        self.board[maxmoves[0]][maxmoves[1]] = 'w'
        return

    def minPlay2(self, newboard, moves, depth, flipped, minVal, maxVal):
        if(depth == 0):
            return min(flipped)
        minscore = 9223372036854775807
        for i in moves:
            newBoard = self.updateBoard(i[0],i[1], "b", newboard)
            newMoves, newflipped = self.getPossibleMoves(newBoard, "b")
            for move in newMoves:
                score = self.maxPlay2(newBoard, moves, depth-1, newflipped, minVal, maxVal)
                if minVal == -1:
                    minVal = score
                    continue
                if minscore < maxVal:
                    break
                elif score < minscore: 
                    minscore = score
        return minscore

    def maxPlay2(self, newboard, moves, depth, flipped, minVal, maxVal):
        if(depth == 0):
            return max(flipped)
        maxscore = 0
        for i in moves:
            newBoard = self.updateBoard(i[0],i[1], "w", newboard)
            newMoves, newflipped = self.getPossibleMoves(newBoard, "w")
            for move in newMoves:
                score = self.minPlay2(newBoard, moves, depth-1, newflipped, minVal, maxVal)
                if maxVal == -1:
                    maxVal = score
                    continue
                if maxscore > minVal:
                    break
                if score > maxscore: 
                    maxscore = score
        return maxscore

    def minimax(self, moves, flipped):
        maxscores = 0
        maxmoves = []
        for i in (range(len(flipped))):
            if flipped[i] > maxscores :
                maxscores = flipped[i]
                maxmoves = moves[i]
        turtle.goto(maxmoves[1]+0.5, maxmoves[0]+0.5)
        turtle.dot(50, 'white')
        x,y = self.isValidMove(self.board, maxmoves[0], maxmoves[1], "w")
        for i in x:
            turtle.goto(i[1]+0.5, i[0]+0.5)
            turtle.dot(50, 'white')
            self.board[i[0]][i[1]] = "w"
        self.board[maxmoves[0]][maxmoves[1]] = 'w'
        return

    def minimax_v2(self, moves, flipped):
        maxscore = 0
        maxmoves = []
        maxDepth = 2
        for i in moves:
            newBoard = self.getNewBoard(i[0], i[1], "w")
            newMoves, newflipped = self.getPossibleMoves(newBoard, "w")
            for move in newMoves:
                score = self.minPlay(newBoard, moves, maxDepth-1, newflipped)
                if score > maxscore: 
                    maxscore = score
                    maxmoves = move

        turtle.goto(maxmoves[1]+0.5, maxmoves[0]+0.5)
        turtle.dot(50, 'white')
        x,y = self.isValidMove(self.board, maxmoves[0], maxmoves[1], "w")
        
        for i in x:
            turtle.goto(i[1]+0.5, i[0]+0.5)
            turtle.dot(50, 'white')
            self.board[i[0]][i[1]] = "w"
        self.board[maxmoves[0]][maxmoves[1]] = 'w'
        return

    def getNewBoard(self, x, y, color):
        newboard = deepcopy(self.board)
        # new_x,new_y = self.isValidMove(self.board, x, y, color)
        
        # for i in new_x:
        #     newboard[i[0]][i[1]] = "w"
        # newboard[x][y] = 'w'
        newboard[x][y] = color
        return newboard

    def updateBoard(self, x, y, color, board):
        newboard = board
        newboard[x][y] = color
        return newboard

    def minPlay(self, newboard, moves, depth, flipped):
        if(depth == 0):
            return min(flipped)
        minscore = 9223372036854775807
        for i in moves:
            newBoard = self.updateBoard(i[0],i[1], "b", newboard)
            newMoves, newflipped = self.getPossibleMoves(newBoard, "b")
            for move in newMoves:
                score = self.maxPlay(newBoard, moves, depth-1, newflipped)
                if score < minscore: 
                    minscore = score
        return minscore

    def maxPlay(self, newboard, moves, depth, flipped):
        if(depth == 0):
            return max(flipped)
        maxscore = 0
        for i in moves:
            newBoard = self.updateBoard(i[0],i[1], "w", newboard)
            newMoves, newflipped = self.getPossibleMoves(newBoard, "w")
            for move in newMoves:
                score = self.minPlay(newBoard, moves, depth-1, newflipped)
                if score > maxscore: 
                    maxscore = score
        return maxscore

    def getPossibleMoves(self, board, color):
        board_array = []
        poss_moves = []
        num_flip = []
        row = 0
        for i in board:
            col = 0
            for j in i:
                board_array.append((row, col))
                col += 1
            row += 1
        for k in board_array:
            to_flip,flipped = self.isValidMove(board, k[0], k[1], color)
            if to_flip != False:
                poss_moves.append(k)
                num_flip.append(flipped)
        return poss_moves,num_flip

    def isValidMove(self, board, row, col, color):
        if color == "b":
            opp = "w"
        else:
            opp = "b"
        tiles_to_flip = []
        tiles_flipped = 0
        invalid = 0
        # check if spot is empty
        if board[row][col] == 0:
            # check for around spot
            invalid = 0
            for i in [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]:
                currow = row + i[0]
                curcol = col + i[1]
                if currow < 0 or currow > 7 or curcol < 0 or curcol > 7:
                    invalid += 1
                else:
                    if board[currow][curcol] == opp:
                        while board[currow][curcol] != color:
                            currow += i[0]
                            curcol += i[1]
                            if currow < 0 or currow > 7 or curcol < 0 or curcol > 7:
                                invalid += 1
                                break
                            else:
                                # if enclosed
                                if board[currow][curcol] == color:
                                    board[row][col] = color
                                    # backtrack now
                                    currow -= i[0]
                                    curcol -= i[1]
                                    while board[currow][curcol] != color:
                                        tiles_to_flip.append((currow, curcol))
                                        tiles_flipped += 1
                                        currow -= i[0]
                                        curcol -= i[1]
                                    board[row][col] = 0
                                    break
                    else:
                        invalid += 1
            if invalid == 8:
                return False, False
            else:
                return tiles_to_flip,tiles_flipped
        else:
            return False, False

    def winner(self):
        p1 = 0
        p2 = 0
        for i in self.board():
            for j in i:
                if j == "b":
                    p1 += 1
                elif j == "w":
                    p2 += 1
        if p1 > p2:
            return "Player 1 wins. "
        else:
            return "Player 2 wins. "

def main():
    game = Othello()
    end = False
    while not end:
        p1 = game.player1()
        p2 = game.player2()
        if p1 == False and p2 == False:
            prompt = turtle.textinput("Othello", game.winner() + "Do you want to play again? (Type yes or no)")
            if prompt == "no":
                exit()
            else:
                game = Othello()

if __name__ == "__main__":
    main()
