import tkinter as tk  # import the tkinter module as tk


class App():
    def __init__(self, c4):
        # initialize all the buttons labels on the second page of the game.
        self.tk = tk.Tk()  # initialize the widget of the overall window.
        self.canvas = tk.Canvas(self.tk,
                                width=50 * c4.BOARD_COLUMNS,
                                height=50 * c4.BOARD_ROWS,
                                borderwidth=0,
                                highlightthickness=0)
        # initialize the window
        self.canvas.pack(fill="both", expand="true")
        # use pack method to insert the canvas into the window.
        self.dp = 1  # set the default mode to "drop"
        self.c4 = c4  # the parameter c4 contains the game board.
        self.help = tk.Label(self.tk, text="Choose Column & Press <ENTER>")
        # prompt the user the rules.
        self.help.pack()  # insert the label into the window.

        self.player = tk.Label(self.tk, text="Player 1")
        # specify what to display in this label.
        self.player.pack()
        # organizes widgets in blocks before placing them in the parent widget.
        self.entry = tk.Entry(self.tk)
        self.entry.bind("<Return>", lambda x: self.isValid())
        self.entry.pack(side="top")
        # determines which side of the parent widget packs against.
        self.valid = tk.Label(self.tk, text="", foreground="red")
        # specify what to display in this label.
        self.valid.pack()
        # organizes widgets in blocks before placing them in the parent widget.
        self.isValid1 = 0
        self.reset = tk.Button(self.tk, text="Reset game",
                               command=self.resetGame)
        # specify what to display in this label.
        self.reset.pack(side="left")
        # determines which side of the parent widget packs against.
        self.drop1 = tk.Button(self.tk, text="Drop", command=self.changeD)
        # specify what to display in this label.
        self.drop1.pack(side="right")
        # determines which side of the parent widget packs against.
        self.pop1 = tk.Button(self.tk, text="Pop", command=self.changeP)
        # specify what to display in this label.
        self.pop1.pack(side="right")
        # determines which side of the parent widget packs against.
        self.quit = tk.Button(self.tk, text="exit", command=self.tk.destroy)
        # specify what to display in this label.
        self.quit.pack(side="left")
        # determines which side of the parent widget packs against.

        self.rect = {}
        self.oval = {}
        self.triangle = {}
        self.tk.title("Connect 4")
        # initialize the title of the second window.
        self.cellwidth = 50  # initialize the width of the ball.
        self.cellheight = 50  # initialize the y radius of the ball.
        self.board = c4.new_game()  # call the new game to get the game board.

        for column in range(c4.BOARD_COLUMNS):
            # use for loop to visualize the game board.
            for row in range(c4.BOARD_ROWS):
                # use for loop to visualize the game board.
                x1 = column * self.cellwidth
                # get the x axis of the position of the ball and rectangular.
                y1 = row * self.cellheight
                # get the y axis of the position of the ball and rectangular.
                x2 = x1 + self.cellwidth
                # get the x axis of the position of the ball and rectangular.
                y2 = y1 + self.cellheight
                # get the y axis of the position of the ball and rectangular.
                self.rect[row, column] = self.canvas.create_rectangle(x1, y1,
                                                                      x2, y2,
                                                                      fill="p"
                                                                           "i"
                                                                           "n"
                                                                           "k",
                                                                      tags="r"
                                                                           "e"
                                                                           "c"
                                                                           "t")
                # draw the rectangles on the initial game board.
                self.oval[row, column] = self.canvas.create_oval(x1 + 2,
                                                                 y1 + 2,
                                                                 x2 - 2,
                                                                 y2 - 2,
                                                                 fill="pink",
                                                                 tags="oval")
            # draw the circles on the initial game board.

    def resetGame(self):
        # rest the second page if the user click the reset button.
        self.canvas.itemconfig("oval",
                               fill="pink")
        # change the background back to pink.
        self.player["text"] = "Player 1"
        # initialize the turn to player1
        self.board = self.c4.new_game()
        # get the new game board.
        self.help[
            "text"] = "Choose Column & Press <ENTER>"
        # change the text back to the game rule.

    def isValid(self):
        # check if the user input column and row are valid.
        try:
            self.isValid1 = int(self.entry.get())
        except:
            self.isValid1 = 0

        if self.isValid1 == "":
            # if there is not yet any input from the user.
            self.valid[
                "text"] = "Please enter something into the entry box"
            # prompt the user to input some column and row number.
            self.valid.after(2000, lambda: self.valid.config(
                text=""))  # check if the input is valid integer.

        elif 1 <= int(
                self.isValid1) <= self.c4.BOARD_COLUMNS:
            # check if the user input is valid.
            if self.c4.winner(self.board) == 0:
                # if there is no winner yet.
                if self.dp == 1:
                    # if the user click drop.
                    self.drop()
                    # implement the drop function.
                elif self.dp == 2:
                    # if the user click the pop button.
                    self.pop()
                    # implement the pop function.
                self.check()
                # check the game status after each input.
                self.display()
                # if the data is valid, display it on the game board.

        else:
            self.valid[
                "text"] = "That move is invalid, please try again"
            # tell user to try again.
            self.valid.after(2000, lambda: self.valid.config(
                text=""))
            # eliminate the content in this label.

        self.entry.delete(0,
                          "end")
        # eliminate the entry box after each entry.

    def changeD(self):
        # check if the user click the drop button.
        self.dp = 1
        # change the status of the mode to 1.

    def changeP(self):
        # check if the user click the pop button.
        self.dp = 2
        # change the status of the mode ot 2.

    def drop(self):
        # run the drop function if the user choose the drop mode.

        col = self.isValid1
        # the drop column is the result after checking isvalid.
        if self.board[0][col - 1][0] == 0:
            self.board = self.c4.drop(self.board, col - 1)
        # implement the drop function from connect four
        self.player["text"] = "Player " + str(self.board[1])
        # prompt the next user for the next move.

    def pop(self):
        # run the pop function if the user choose the pop mode.
        col = self.isValid1
        # the pop column is the result after checking isvalid.
        if self.board[0][col - 1][-1] == self.board[1]:
            # if the choose column is correct player turn.
            self.board = self.c4.pop(self.board, col - 1)
            # implement the pop function.
            self.player["text"] = "Player " + str(self.board[1])
            # prompt the next user for the next move.

    def display(self):
        # reflect the current status of the game board.
        color = ""
        # the initial color is blank.
        for column in range(
                self.c4.BOARD_COLUMNS):
            # use for loop to visualize the game board columns.
            for row in range(
                    self.c4.BOARD_ROWS):
                # use for loop to visualize the game board rows.
                if self.board[0][column][row] == 2:
                    # if the game board position is 2.
                    color = "black"
                    # reflect the game status on the board with a color.
                if self.board[0][column][row] == 1:
                    # if the game board position is 1.
                    color = "white"
                    # reflect the game status on the board with a color.
                if self.board[0][column][row] == 0:
                    # if the game board position is zero.
                    color = "pink"
                    # draw the background color if the data is zero.
                x1 = column * self.cellwidth
                # get to the next column for each loop.
                y1 = row * self.cellheight
                # get to the next row for each loop.
                x2 = x1 + self.cellwidth
                # get to the next column for each loop.
                y2 = y1 + self.cellheight
                # get to the next row for each loop.
                self.oval[row, column] = self.canvas.create_oval(x1 + 2,
                                                                 y1 + 2,
                                                                 x2 - 2,
                                                                 y2 - 2,
                                                                 fill=color,
                                                                 tags="oval")
                # draw the circle with the given row and column.

    def check(self):
        # check if any of the two players win the game, pass if no winner yet.
        if self.c4.winner(self.board) == 1:
            # check if white player is the winner.
            self.help["text"] = "White Player Won !"
            # prompt players that white player won the game.

        if self.c4.winner(self.board) == 2:
            # check if black player is the winner.
            self.help["text"] = "Black Player Won !"
            # prompt players that black player won the game.

        else:  # if winner is not white nor black.
            pass  # pass if there is no player won.

    def run(self):
        self.tk.mainloop()
        # wait for an event to occur process event if the window not closed.


class window1:
    def __init__(self, c4):
        self.tk = tk.Tk()
        self.tk.title("Connect Four")
        # create the title of the game and show it on the top of the window.
        self.label1 = tk.Label(master=self.tk,
                               text="Number of Columns:")
        # specify what to display in this label.
        self.label2 = tk.Label(master=self.tk,
                               text="Number of Rows:")
        # specify what to display in this label.
        self.e1 = tk.Entry(
            master=self.tk)
        # represents the parent window and create the input box.
        self.e2 = tk.Entry(
            master=self.tk)
        # represents the parent window and create the input box.
        self.button1 = tk.Button(master=self.tk,
                                 text="Start Game")
        # specify what to display in this label.
        self.label1.grid(column=0, row=0,
                         columnspan=4)
        # puts the widgets in a 2-dimensional table specify the row and column.
        self.label2.grid(column=0, row=1,
                         columnspan=4)
        # puts the widgets in a 2-dimensional table specify the row and column.
        self.label3 = tk.Label(master=self.tk,
                               text="Please select 6 - 14")
        # specify what to display in this label.
        self.label3.config(bg="red")
        # set the background of the text of label3.
        self.label3.grid(column=0, row=2,
                         columnspan=4)
        # puts the widgets in a 2-dimensional table specify the row and column.
        self.e1.grid(column=4, row=0,
                     columnspan=4)
        # puts the widgets in a 2-dimensional table specify the row and column.
        self.e2.grid(column=4, row=1,
                     columnspan=4)
        # puts the widgets in a 2-dimensional table specify the row and column.
        self.button1.grid(column=4, row=2,
                          columnspan=3)
        # puts the widgets in a 2-dimensional table specify the row and column.
        self.c4 = c4  # initialize the game board in the parameter.
