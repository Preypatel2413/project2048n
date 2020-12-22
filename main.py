import tkinter as tk
import coler as c
import random
class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048 3D")
        self.n=int(input())
        self.mainGrid=tk.Frame(
            self,bg=c.GridColor, bd=3,width=600,height=600
        )
        self.mainGrid.grid(pady=(100,0))
        self.makeGUI()
        self.startGame()

        self.master.bind("<Left>",self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    def makeGUI(self): # making the GUI
        self.cells=[]
        for i in range(self.n):
            row=[]
            for j in range (self.n):
                cellFrame=tk.Frame(
                    self.mainGrid,
                    bg=c.EmptyCellColor,
                    width=600//self.n,
                    height=600//self.n
                )
                cellFrame.grid(row=i,column=j, padx=5, pady=5)
                cellNumber=tk.Label(self.mainGrid, bg=c.EmptyCellColor)
                cellNumber.grid(row=i, column=j)
                cellData={"frame": cellFrame, "number": cellNumber}
                row.append(cellData)
            self.cells.append(row)

        # make score header
        scoreFrame=tk.Frame(self)
        scoreFrame.place(relx=0.5,y=45,anchor="center")
        tk.Label(
            scoreFrame,
            text="Score",
            font=c.ScoreLabelFont
        ).grid(row=0)
        self.scoreLabel=tk.Label(scoreFrame, text="0", font=c.ScoreFont)
        self.scoreLabel.grid(row=1)


    def startGame(self):
        # create matrix
        self.matrix=[[0]*self.n for _ in range(self.n)]

        #fill 2 random cell with 2s
        row=random.randint(0,self.n-1)
        col=random.randint(0,self.n-1)
        self.matrix[row][col]=2
        self.cells[row][col]["frame"].configure(bg=c.CellColors[2])
        self.cells[row][col]["number"].configure(
            bg=c.CellColors[2],
            fg=c.CellNumberColors[2],
            font=c.CellNumberFonts[2],
            text="2"
        )
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CellColors[2])
        self.cells[row][col]["number"].configure(
            bg=c.CellColors[2],
            fg=c.CellNumberColors[2],
            font=c.CellNumberFonts[2],
            text="2"
        )

        self.score = 0

    # Matrix fuctions

    def stack(self):    #Stack : it will make a new matrix in which it will stack numbers on left side and return that new matrix to Matrix
        newMatrix = [[0]*self.n for _ in range(self.n)]
        for i in range(self.n):
            fillPosition=0
            for j in range(self.n):
                if (self.matrix[i][j] != 0):
                    newMatrix[i][fillPosition]=self.matrix[i][j]
                    fillPosition = fillPosition+1
        self.matrix=newMatrix


    def combine(self):      # after stacking the matrix, combine will merge the same numbers
        for i in range(self.n):
            for j in range (self.n-1):
                if self.matrix[i][j] != 0 and self.matrix[i][j]==self.matrix[i][j+1]:
                    self.matrix[i][j] *=2
                    self.matrix[i][j+1] =0
                    self.score +=self.matrix[i][j]


    def reverse(self):    #it will give mirror image of the matrix
        newMatrix = []
        for i in range(self.n):
            newMatrix.append([])
            for j in range(self.n):
                newMatrix[i].append(self.matrix[i][self.n-j-1])
        self.matrix = newMatrix

    def transpose(self):    #it will give transpose of the matrix
        newMatrix=[[0]*self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                newMatrix[i][j]=self.matrix[j][i]
        self.matrix = newMatrix


    # Add new tile

    def addTile(self):
        row = random.randint(0, (self.n)-1)
        col = random.randint(0, (self.n)-1)
        while (self.matrix[row][col] != 0):
            row = random.randint(0, (self.n)-1)
            col = random.randint(0, (self.n)-1)
        self.matrix[row][col] = random.choice([2,4])

    #Update the GUI

    def updateGUI(self):
        for i in range(self.n):
            for j in range(self.n):
                cellValue = self.matrix[i][j]
                if cellValue==0:
                    self.cells[i][j]["frame"].configure(bg=c.EmptyCellColor)
                    self.cells[i][j]["number"].configure(bg=c.EmptyCellColor,text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CellColors[cellValue])
                    self.cells[i][j]["number"].configure(
                        bg=c.CellColors[cellValue],
                        fg=c.CellNumberColors[cellValue],
                        font=c.CellNumberFonts[cellValue],
                        text=str(cellValue)
                    )
        self.scoreLabel.configure(text=self.score)
        self.update_idletasks()


    # arrow press functions

    def left(self,event):
        self.stack()
        self.combine()
        self.stack()
        self.addTile()
        self.updateGUI()
        self.gameOver()


    def right(self,event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.addTile()
        self.updateGUI()
        self.gameOver()

    def up(self,event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.addTile()
        self.updateGUI()
        self.gameOver()

    def down(self,event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.addTile()
        self.updateGUI()
        self.gameOver()


    # check if any move are possible
    def horizMove(self):
        for i in range(self.n):
            for j in range(self.n-1):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False

    def vertiMove(self):
        for i in range(self.n-1):
            for j in range(self.n):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False

    # check game is over
    def gameOver(self):
        if any(2048 in row for row in self.matrix):
            gameOverFrame=tk.Frame(self.mainGrid,borderwidth=2)
            gameOverFrame.place(relx=0.5,rely=0.5,anchor="center")
            tk.Label(
                gameOverFrame,
                text="You Win!!!",
                bg=c.WinnerBG,
                fg=c.GameOverFontColor,
                font=c.GameOverFont
            ).pack()
        elif not any(0 in row for row in self.matrix)and not self.horizMove() and not self.vertiMove():
            gameOverFrame = tk.Frame(self.mainGrid, borderwidth=2)
            gameOverFrame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                gameOverFrame,
                text="You Lose....",
                bg=c.LoserBG,
                fg=c.GameOverFontColor,
                font=c.GameOverFont
            ).pack()


def main():
    Game()

if __name__ =="__main__":
    main()