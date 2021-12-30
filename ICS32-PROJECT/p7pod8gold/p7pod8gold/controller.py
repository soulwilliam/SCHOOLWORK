import connectfour as c4
# import the model file.
import view


# import the view file.


def run(tk):
    # run the program with the widget of window2 as parameter.
    tk.mainloop()
    # wait for an event to occur and process the event if it is not closed.


def get_row_col(e1, e2, tk):
    # open the first window that get user input the column and row.
    if e1.get().isdigit() and e2.get().isdigit():
        # check if the user input is digit.
        c4.BOARD_COLUMNS = int(e1.get())
        # get the column number in the box from the user.
        c4.BOARD_ROWS = int(e2.get())
        # get the row number in the box from the user.
        if 6 <= c4.BOARD_COLUMNS <= 14 and 6 <= c4.BOARD_ROWS <= 14:
            # check if the two numbers are valid.
            tk.destroy()
            # close the first window.
    else:
        pass

        # pass the function if the user input is not qualified.


if __name__ == "__main__":
    x = view.window1(c4)
    # open the first window to get col and row number.
    x.button1["command"] = lambda: get_row_col(x.e1, x.e2, x.tk)
    # give the button new command
    run(x.tk)
    # run the program with the widget of window2 as parameter.
    view.App(c4).run()
    # run the program and create the second page of the program.
