import p8view as v  # import the view file.


class Controller:
    def __init__(self):
        # initialize the window.
        self.view1 = v.View1().tk.mainloop()
        # wait for an event to occur process event if the window not closed.
        self.view2 = v.View2().tk.mainloop()
        # wait for an event to occur process event if the window not closed.


if __name__ == '__main__':
    # run the two window respectively.
    Controller()
