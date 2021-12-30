# spots_game.py
#
# ICS 32 Winter 2019
# Code Example
#
# This module implements the "view" for our Spots game.  The job of a
# view is to focus on how the game looks and feels -- how it's drawn and
# how the user interacts with it -- while ignoring the details about the
# game's mechanics.  It's not uncommon for the view to hold a reference
# back to the model, which we're doing here.  As the user does things,
# they'll generate events in the view, which will then be sent to the
# model as higher-level operations that affect the game's mechanics.
#
# Note, too, that we've taken a keener eye toward the design of this
# example, by doing a couple of additional things:
#
# * We implemented our game in a class, rather than in a function.  This
#   gives us a natural way to break it up into many functions, while
#   still preserving their ability to share the important information
#   between them (in the form of the "self" parameter that they all
#   share).
#
# * We broke up our game loop into calls to methods in this class.  This
#   took what would have been a long, complex method and made it much
#   shorter.  By giving names to these "helper" methods, we've made
#   clearer the pattern that shows up in our design.  Going forward,
#   if we were to add new features, they would have a place where they
#   belong.  For example, new user inputs would be dealt with in
#   _handle_events; changes to how things are drawn would be dealt with
#   in _redraw; and so on.

import connectfour as c4
import pygame
import sys

white = (255, 255, 255)  # create color for text.
green = (0, 150, 0)  # create color for text.
blue = (0, 0, 128)  # create color for text.
grey = (127, 127, 127)  # create color for text.
black = (0, 0, 0)  # create color for text.
purple = (100, 0, 200)  # create color for text.
p1_red = (150, 0, 0)  # create color for text.
p2_yellow = (255, 255, 0)  # create color for text.

radiusy = 37  # circle radius
radiusx = radiusy  # x radius equals y radius


class Connect4Game:  # make the game class
    def __init__(self):
        self._running = True  # check if the game is still running.
        self.tf2 = True  # check the layer
        self.d = 'Enter Column (6-10) & press <ENTER>: '  # create text to prompt user input
        self.d2 = 'Row Number(6 - 10): '  # create text to prompt user input
        self.d3 = 'Enter Column (6-10) & press <ENTER>: '  # create text to prompt user input
        self.d4 = 'PLease Enter a valid number(6 - 10): '  # create text to prompt user input
        self.w = 700  # original width
        self.g = green  # color for the text
        self.r = p1_red  # create color for circle
        self.h = 750  # original high
        self.tf = True  # check layer
        self.New_game = 0  # initialize game number
        self.column = 0  # initialize column number
        self.row = 0  # initialize row number
        self.page = 1  # initialize page
        self.dp = 1  # initialize drop as the default option
        self.t = "  Red's  turn  "  # subtitle for turn
        self.t2 = "Yellow's turn"  # subtitle for turn
        self.t1 = "  Red's  turn  "  # subtitle for turn
        pygame.init()  # initialize pygame
        self.win = pygame.mixer.Sound('music.ogg')  # open the music file
        self.win.play()  # add song and play

    def run(self):
        pygame.init()  # initialize pygame

        self._resize_surface((self.w, self.h))  # resize function

        while self._running:  # check if game is running
            clock = pygame.time.Clock()  # set the refresh frequency
            clock.tick(80)  # make the ball move smoothly

            self._handle_events()  # call function
            self._redraw()  # draw initial background
            if self.tf:  # check user input
                self.ask_col()
                self.ask_row()

            c4.BOARD_COLUMNS = self.column
            c4.BOARD_ROWS = self.row
            self.w = radiusx * c4.BOARD_COLUMNS * 2  # set the width of the working window
            self.h = radiusy * (c4.BOARD_ROWS + 1) * 2  # set the height of the working window
            self._resize_surface((self.w, self.h))  # open the game window
            self._redraw()  # draw initial background
            self._open()  # open the game program

        pygame.quit()  # quit the game when done

    def _redraw(self):  # draw initial background
        surface = pygame.display.get_surface()  # get current game surface
        surface.fill(pygame.Color(100, 0, 200))  # fill back ground with color
        pygame.display.flip()  # refresh the current page

    def _handle_events(self):  # check if the user need to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            if event.type == pygame.VIDEORESIZE:  # resize the window if needed
                self._resize_surface(event.size)

    def _end_game(self):  # set the game status to stop running
        self._running = False

    def _resize_surface(self, size):  # resize the window of the game
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def ask_col(self):
        """Get the valid column number of the game window."""
        self.tf2 = True
        surface = pygame.display.get_surface()  # get current game surface
        font = pygame.font.Font('freesansbold.ttf', 32)  # create font type for text.

        while self.tf2:
            surface.fill(pygame.Color(100, 0, 200))
            text = font.render(self.d, True, black)  # create font type for text.
            textRect = text.get_rect()  # create font type for text.
            textRect.center = (self.w / 2, self.h / 2)  # position for text.
            surface.blit(text, textRect)  # print out the text.
            pygame.display.flip()  # refresh the current page

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keys2 = [eval('pygame.K_' + str(i)) for i in range(10)]  # get list of all possible click

                    if event.key in keys2:  # check user column input
                        self.d += str(int(event.key) - 48)
                        self.column *= 10
                        self.column += int(event.key) - 48
                        pygame.display.flip()  # refresh the current page
                    if event.key == pygame.K_RETURN:  # check user keyboard input
                        if self.column < 6 or self.column > 10:  # check if user input is valid
                            self.column = 0
                            self.d = self.d4
                            self.ask_col()
                        else:  # check if user input is valid
                            self.d = self.d2

                            self.tf2 = False

    def ask_row(self):
        """Get the valid column number of the game window."""
        self.tf2 = True
        surface = pygame.display.get_surface()  # get current game surface
        font = pygame.font.Font('freesansbold.ttf', 32)  # create font type for text.

        while self.tf2:
            surface.fill(pygame.Color(100, 0, 200))
            text = font.render(self.d, True, black)  # create font type for text.
            textRect = text.get_rect()  # create font type for text.
            textRect.center = (self.w / 2, self.h / 2)  # position for text.
            surface.blit(text, textRect)  # add explanation text

            pygame.display.flip()  # refresh the current page

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keys2 = [eval('pygame.K_' + str(i)) for i in range(10)]

                    if event.key in keys2:  # check user keyboard input
                        self.d += str(int(event.key) - 48)  # get the user instruction
                        self.row *= 10
                        self.row += int(event.key) - 48  # get the user instruction
                        pygame.display.flip()  # refresh the current page
                    if event.key == pygame.K_RETURN:  # check user keyboard input
                        if self.row < 6 or self.row > 10:  # check if user input is valid
                            self.row = 0
                            self.d = self.d4
                            self.ask_row()
                        else:  # check if user input is valid
                            self.d = self.d3
                            self.tf2 = False
                            self.tf = False

    def _open(self):
        self.New_game = c4.new_game()  # get initial game board
        myimage = pygame.image.load('start.png')  # load the image
        surface = pygame.display.get_surface()  # get current game surface
        surface.blit(myimage, [self.w / 3 - 69, self.h / 2])  # draw the image at this place
        pygame.display.flip()  # refresh the current page

        myimage2 = pygame.image.load('header_logo.png')  # load the image
        surface = pygame.display.get_surface()  # get current game surface
        surface.blit(myimage2, [self.w / 2 - 280, self.h / 4 - 50])  # draw the image at this place
        pygame.display.flip()  # refresh the current page

        myimage3 = pygame.image.load('exit.png')  # load the image
        surface = pygame.display.get_surface()  # get current game surface
        surface.blit(myimage3, [self.w / 3 * 2 - 70, self.h / 2])  # draw the image at this place
        pygame.display.flip()  # refresh the current page

        while True:
            for event in pygame.event.get():  # get event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.page == 1:  # check the current working page
                        if self.w / 3 - 69 <= event.pos[0] <= self.w / 3 + 69 and self.h / 2 <= event.pos[
                            1] <= self.h / 2 + 138:  # decide if the click is ok.
                            self.game_page()
                            self.page = 2

                        if self.w / 3 * 2 - 70 <= event.pos[0] <= self.w / 3 * 2 + 70 and self.h / 2 <= event.pos[
                            1] <= self.h / 2 + 140:  # check if the user click the image.
                            pygame.quit()  # quit the game.
                            sys.exit()  # quit the system.

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:  # check user keyboard input
                        self.two_input()

                    if self.page == 2:  # check the current working page
                        if event.key == pygame.K_SPACE:  # check user keyboard input

                            self.page = 3  # change the page record
                            self.game_page()

                            i = radiusy
                            j = radiusx * 3
                            for y in range(c4.BOARD_ROWS):
                                for x in range(c4.BOARD_COLUMNS):
                                    pygame.draw.circle(surface, (0, 0, 0), (i, j), radiusy)

                                    i += radiusy * 2
                                    pygame.display.flip()  # refresh the current page
                                i = radiusy
                                j += radiusx * 2
                            pygame.display.flip()  # refresh the current page

                    if self.page == 3:  # check the current working page
                        self.key_drop(self.New_game)

    def key_drop(self, New_game):
        """Display the outcome after the user input."""

        while True:
            surface = pygame.display.get_surface()  # get current game surface
            font3 = pygame.font.Font('freesansbold.ttf', 30)  # create font type for text.
            text3 = font3.render('drop', True, black, self.g)  # create font type for text.
            textRect3 = text3.get_rect()  # create font type for text.
            textRect3.center = (32, 15)  # position for text.
            surface.blit(text3, textRect3)  # add explanation text

            font4 = pygame.font.Font('freesansbold.ttf', 30)  # create font type for text.
            text4 = font4.render('pop', True, black, self.r)  # create font type for text.
            textRect4 = text4.get_rect()  # create font type for text.
            textRect4.center = (100, 15)  # position for text.
            surface.blit(text4, textRect4)  # add explanation text

            font5 = pygame.font.Font('freesansbold.ttf', 30)  # create font type for text.
            text5 = font5.render(self.t, True, black, purple)  # create font type for text.
            textRect5 = text5.get_rect()  # create font type for text.
            textRect5.center = (self.w - 100, 15)  # position for text.
            surface.blit(text5, textRect5)  # add explanation text

            if self.New_game.turn == 1:  # check the current player
                self.t = self.t1
            elif self.New_game.turn == 2:  # check the current player
                self.t = self.t2
            pygame.display.flip()  # refresh the current page

            for event in pygame.event.get():  # get event

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.page == 3:  # check the current working page
                        if 0 <= event.pos[0] <= 64 and 0 <= event.pos[1] <= 30:  # check if the user click the image.
                            self.g = (0, 255, 0)
                            self.r = p1_red
                            pygame.display.flip()  # refresh the current page
                            self.dp = 1
                        if 75 <= event.pos[0] <= 125 and 0 <= event.pos[1] <= 30:  # check if the user click the image.
                            self.g = green
                            self.r = (255, 0, 0)
                            pygame.display.flip()  # refresh the current page
                            self.dp = 2
                if event.type == pygame.KEYDOWN:
                    if c4.BOARD_COLUMNS >= 10:  # check user keyboard column input
                        keys = [eval('pygame.K_' + str(i)) for i in range(10)]
                    else:  # check user keyboard column input
                        keys = [eval('pygame.K_' + str(i + 1)) for i in range(c4.BOARD_COLUMNS)]
                    if event.key in keys:  # check user keyboard input
                        column = int(event.key) - 49  # get the correct user input
                        if column == -1:  # check user keyboard column input
                            column = 9
                        while c4.winner(New_game) == 0:  # check if there is no winner yet
                            if self.dp == 1:  # check if the mode is drop
                                if 0 in self.New_game.board[column]:
                                    self.New_game = c4.drop(New_game, column)

                            if self.dp == 2:  # check if the mode is pop
                                if self.New_game.turn == self.New_game.board[column][self.row - 1]:
                                    self.New_game = c4.pop(New_game, column)
                            self.refresh()  # refresh window if needed

                            self.key_drop(self.New_game)  # drop a new icon
                self.check(New_game)

    def check(self, New_game):

        if c4.winner(New_game) == 1:
            self._redraw()
            myimage = pygame.image.load('red.png')  # load the image
            surface = pygame.display.get_surface()  # get current game surface
            surface.blit(myimage, [self.w / 2 - 99, 100])  # draw the image at this place
            pygame.display.flip()  # refresh the current page
            self.back()

        elif c4.winner(New_game) == 2:
            self._redraw()
            myimage = pygame.image.load('yellowwin.png')  # load the image
            surface = pygame.display.get_surface()  # get current game surface
            surface.blit(myimage, [self.w / 2 - 150, 100])  # draw the image at this place
            pygame.display.flip()  # refresh the current page
            self.back()

    def back(self):
        myimage5 = pygame.image.load('congrat.png')  # load the image
        surface = pygame.display.get_surface()  # get current game surface
        surface.blit(myimage5, [self.w / 2 - 600, 50])  # draw the image at this place
        pygame.display.flip()  # refresh the current page

        myimage3 = pygame.image.load('exit.png')  # load the image
        surface = pygame.display.get_surface()  # get current game surface
        surface.blit(myimage3, [self.w / 3 * 2 - 70, self.h / 2])  # draw the image at this place
        pygame.display.flip()  # refresh the current page

        myimage = pygame.image.load('return.png')  # load the image
        surface = pygame.display.get_surface()  # get current game surface
        surface.blit(myimage, [self.w / 3 - 70, self.h / 2])  # draw the image at this place
        pygame.display.flip()  # refresh the current page
        while True:
            for event in pygame.event.get():  # get event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.w / 3 - 70 <= event.pos[0] <= self.w / 3 + 70 and self.h / 2 <= event.pos[
                        1] <= self.h / 2 + 140:  # decide if the click is ok.
                        Connect4Game().run()  # begin the program.
                    if self.w / 3 * 2 - 70 <= event.pos[0] <= self.w / 3 * 2 + 70 and self.h / 2 <= event.pos[
                        1] <= self.h / 2 + 140:  # decide if the click is ok.
                        pygame.quit()  # quit the game.
                        sys.exit()  # quit the system.

    def refresh(self):
        i = radiusy
        j = radiusx * 3
        surface = pygame.display.get_surface()  # get current game surface

        for y in range(c4.BOARD_ROWS):
            for x in range(c4.BOARD_COLUMNS):
                if self.dp == 1:  # check the working mode is pop or drop
                    if self.New_game[0][x][y] == 1:
                        pygame.draw.circle(surface, (255, 0, 0), (i, j), radiusy)
                        face = pygame.image.load('trump.png')  # load the image
                        surface = pygame.display.get_surface()  # get current game surface
                        surface.blit(face, [i - 37, j - 37])  # draw the image at this place
                        pygame.display.flip()  # refresh the current page
                        i += radiusy * 2  # add the x coordinate

                    elif self.New_game[0][x][y] == 2:  # add the x coordinate
                        pygame.draw.circle(surface, (255, 255, 0), (i, j), radiusy)
                        face2 = pygame.image.load('putin.png')  # load the image
                        surface = pygame.display.get_surface()  # get current game surface
                        surface.blit(face2, [i - 33, j - 33])  # draw the image at this place
                        pygame.display.flip()  # refresh the current page
                        i += radiusy * 2  # add the x coordinate
                    else:
                        i += radiusy * 2  # add the x coordinate

                elif self.dp == 2:
                    if self.New_game[0][x][y] == 0:
                        pygame.draw.circle(surface, (0, 0, 0), (i, j), radiusy)
                        i += radiusy * 2  # add the x coordinate
                    elif self.New_game[0][x][y] == 1:
                        pygame.draw.circle(surface, (255, 0, 0), (i, j), radiusy)
                        face = pygame.image.load('trump.png')  # load the image
                        surface = pygame.display.get_surface()  # get current game surface
                        surface.blit(face, [i - 37, j - 37])  # draw the image at this place
                        pygame.display.flip()  # refresh the current page
                        i += radiusy * 2  # add the x coordinate
                    elif self.New_game[0][x][y] == 2:
                        pygame.draw.circle(surface, (255, 255, 0), (i, j), radiusy)
                        face2 = pygame.image.load('putin.png')  # load the image
                        surface = pygame.display.get_surface()  # get current game surface
                        surface.blit(face2, [i - 33, j - 33])  # draw the image at this place
                        pygame.display.flip()  # refresh the current page
                        i += radiusy * 2  # add the x coordinate
                    else:
                        i += radiusy * 2  # add the x coordinate

                pygame.display.flip()  # refresh the current page
            i = radiusy
            j += radiusx * 2

    def game_page(self):
        surface = pygame.display.get_surface()  # get current game surface
        surface.fill(pygame.Color(0, 255, 255))  # fill color for surface

        if self.page != 3:  # check the current working page
            rule = pygame.image.load('rules.png')
            surface = pygame.display.get_surface()  # get current game surface
            surface.blit(rule, [self.w / 2 - 240, self.h / 2 - 218])  # add explanation text

        pygame.display.flip()  # refresh the current page


if __name__ == '__main__':
    Connect4Game().run()  # begin the program.
