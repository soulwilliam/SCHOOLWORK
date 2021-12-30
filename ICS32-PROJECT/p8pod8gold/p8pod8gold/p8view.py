import p8model as m
import time
import tkinter as tk
from collections import namedtuple

# set the model class
m = m.Model()


class View1:
    def __init__(self):
        global m
        # global m used to check if the input is valid.
        self.tk = tk.Tk()
        self.tk.title('TV Search')
        # name the window.
        self.m = m

        self.label = tk.Label(master=self.tk, text='TV Name:')
        # initialize all the label on the first window of the game.

        self.label.grid(column=0, row=0)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.label1 = tk.Label(master=self.tk, text='')
        # initialize all the label on the first window of the game.
        self.label1.grid(column=0, row=1, columnspan=2)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.e = tk.Entry(master=self.tk)
        # represents the parent window and create the input box.
        self.e.grid(column=1, row=0)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.b = tk.Button(master=self.tk, text='search', command=self.search)
        self.b.grid(column=2, row=0)
        # puts the widgets in a 2-dimensional table specify the row and column.

    def search(self):
        tv_name = self.e.get()
        # get the number in the entry box.
        self.m.search_tv(tv_name)
        self.tk.destroy()
        # close the first window.


class View2:
    def __init__(self):
        global m
        self.tk = tk.Tk()
        # initialize the window.
        self.tk.title('All Episodes')
        # give the second window a name.

        self.scrollbar = tk.Scrollbar(self.tk)
        # create the scroll bar for all episodes.
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # pack the bar to the right side of the window
        self.listbox = tk.Listbox(self.tk, yscrollcommand=self.scrollbar.set,
                                  selectmode=tk.MULTIPLE)
        # enable multiple choice.
        self.key = list(m.dict.keys())
        for i in self.key:
            self.listbox.insert(tk.END, i)
            # insert the entry box.
            for j in m.dict[i]:
                self.listbox.insert(tk.END, j)
                # insert the entry box.
            self.listbox.insert(tk.END, '')
            # insert the entry box.
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        # pack the entry box.
        self.scrollbar.config(command=self.listbox.yview)
        # open the third window for user choice of episodes.
        View3().tk.mainloop()


class View3:
    def __init__(self):
        global m

        self.tk = tk.Tk()
        # open the third window for user input.
        self.tk.title('Select 5 Episodes:')
        # tell user the rules.
        self.count = 0
        # no episode has been chosen.
        self.text1 = ''
        self.work = True
        # the program is running.

        self.label = tk.Label(master=self.tk, text='Season Number:')
        # initialize all the label on the third window of the game.
        self.label.grid(column=0, row=0)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.label2 = tk.Label(master=self.tk, text='Episode Number:')
        # initialize all the label on the third window of the game.
        self.label2.grid(column=0, row=1)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.label3 = tk.Label(master=self.tk, text='')
        # initialize all the label on the third window of the game.
        self.label3.grid(column=1, row=2)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.label4 = tk.Label(master=self.tk,
                               text='Select 5 episodes\nWhen 5 valid '
                                    'episodes are selected\nthe download '
                                    'button will be shown\nepisode after '
                                    '5 cannot be added')
        # initialize all the label on the third window of the game.
        self.label4.grid(column=0, row=2)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.label5 = tk.Label(master=self.tk, text='')
        # initialize all the label on the third window of the game.
        self.label5.grid(column=0, row=4)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.label6 = tk.Label(master=self.tk, text='')
        # initialize all the label on the third window of the game.
        self.label6.grid(column=1, row=5)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.label7 = tk.Label(master=self.tk, text='')
        # initialize all the label on the third window of the game.
        self.label7.grid(column=0, row=5)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.e = tk.Entry(master=self.tk)
        # represents the parent window and create the input box.
        self.e.grid(column=1, row=0)
        # puts the widgets in a 2-dimensional table specify the row and column.
        self.e2 = 0

        self.e2 = tk.Entry(master=self.tk)
        # represents the parent window and create the input box.
        self.e2.grid(column=1, row=1)
        # puts the widgets in a 2-dimensional table specify the row and column.

        self.b = tk.Button(master=self.tk, text='add', command=self.search)
        self.b.grid(column=1, row=3)
        # puts the widgets in a 2-dimensional table specify the row and column.
        self.b2 = 0

    def search(self):
        if self.work:
            num1 = self.e.get()
            # get the input from the first entry box.
            num2 = self.e2.get()
            # get the input from the second entry box.
            if num1.isdigit() and num2.isdigit():
                # check if both the season and episode number are valid.
                x = m.get_season(num1, num2)
                # check if the season and episode number are valid
                if x == 0:
                    self.text1 = 'invalid episode or season number'
                    # tell user if it is invalid.
                else:
                    self.count += 1
                    # change the count to 1 if it is valid.
                    self.text1 = 'add successfully'
                    # tell user if it is valid.
            else:
                self.text1 = 'invalid episode or season number'

            if self.count == 5:
                self.b2 = tk.Button(master=self.tk, text='download',
                                    command=self.download)
                self.b2.grid(column=0, row=3)
                # puts the widgets in a 2-dimensional table.
                self.label5['text'] = 'File name you want:'
                self.e2 = tk.Entry(master=self.tk)
                # represents the parent window and create the input box.
                self.e2.grid(column=1, row=4)
                # puts the widgets in a 2-dimensional table.
                m.sort_by_time()
                self.work = False
                self.text1 = 'reached 5'
            self.label3['text'] = self.text1

    def download(self):
        # download the data and write into a file.
        filename = self.e2.get()
        # get the content in the second entry.
        if filename == '':
            # check if the file exist.
            self.label6['text'] = 'Invalid filename'
            # prompt user for another file name.
        else:
            m.download(filename)
            # write the data into the file if the name is valid.
            self.label7['text'] = 'Download Successfully\n' \
                                  'in your workplace\nof the program'
            # tell user when it is done.
