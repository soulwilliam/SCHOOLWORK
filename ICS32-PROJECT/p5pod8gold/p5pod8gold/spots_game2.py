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

import random
import sys

import pygame
import spots2

white = (255, 255, 255)  # create color for text.
green = (0, 255, 0)  # create color for text.
blue = (0, 0, 128)  # create color for text.
grey = (127, 127, 127)  # create color for text.
black = (0, 0, 0)  # create color for text.
red = (255, 0, 0)  # create color for text.
color_list = [(255, 0, 0), (0, 0, 0), (0, 0, 128), (0, 255, 0), (255, 255, 255), (127, 127, 127), (0, 0, 45),
              (60, 20, 0), (0, 180, 90), (90, 255, 0), (255, 30, 0), (0, 0, 128)]  # create the color list.


class SpotsGame:
    def __init__(self):
        self._running = True
        self._state = spots2.SpotsState()
        self.color = (0, 0, 0)  # initialize color
        self.level = 10  # initialize level to level one
        self.rule = "Eliminate all balls"  # create a string for title
        self.d = "Level One"  # create a string for level
        self.c = 'Press LEFT or RIGHT to change ball color you like.'  # tell users how ot change color

        pygame.init()
        self.win = pygame.mixer.Sound('music.ogg')  # open the music file
        self.win.play()  # add song and play

    def run(self) -> None:
        pygame.init()

        self._resize_surface((600, 600))

        clock = pygame.time.Clock()
        for i in range(self.level):
            self._state.createten((random.uniform(0, 1), random.uniform(0, 1)), self.d)
        while self._running:
            clock.tick(80)    # make the ball move more smooth.
            self._handle_events()
            self._redraw()
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._on_mouse_button(event.pos)
            elif event.type == pygame.KEYDOWN:  # change spot color
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # check keyboard type.
                    self.color = random.choice(color_list)  # change spot color

        self._move_spots()

    def _redraw(self) -> None:
        surface = pygame.display.get_surface()

        surface.fill(pygame.Color(255, 255, 0))

        self._text()  # add text to screen
        self._draw_spots()

        pygame.display.flip()

    def _draw_spots(self) -> None:
        for spot in self._state.all_spots():
            self._draw_spot(spot)

    def _draw_spot(self, spot: spots2.Spot) -> None:
        frac_x, frac_y = spot.center()

        topleft_frac_x = frac_x - spot.radius()
        topleft_frac_y = frac_y - spot.radius()

        frac_width = spot.radius() * 2
        frac_height = spot.radius() * 2

        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()

        topleft_pixel_x = topleft_frac_x * width
        topleft_pixel_y = topleft_frac_y * height

        pixel_width = frac_width * width
        pixel_height = frac_height * height

        pygame.draw.ellipse(
            surface, self.color,  # color ball
            pygame.Rect(
                topleft_pixel_x, topleft_pixel_y,
                pixel_width, pixel_height))

    def _end_game(self) -> None:
        self._running = False

    def _text(self):
        surface = pygame.display.get_surface()
        font = pygame.font.Font('freesansbold.ttf', 32)  # create font type for text.
        font2 = pygame.font.Font('freesansbold.ttf', 20)  # create font type for text.
        font3 = pygame.font.Font('freesansbold.ttf', 25)  # create font type for text.
        font4 = pygame.font.Font('freesansbold.ttf', 45)  # create font type for text.

        text = font.render(self.d, True, blue)  # create font type for text.
        text2 = font2.render(self.c, True, blue)  # create font type for text.
        text4 = font4.render(self.rule, True, white, grey)  # create font type for text.

        textRect = text.get_rect()  # create font type for text.
        textRect2 = text2.get_rect()  # create font type for text.

        textRect4 = text2.get_rect()  # create font type for text.
        textRect4.center = (350, 200)  # position for text.

        textRect.center = (300, 300)  # position for text.
        textRect2.center = (300, 400)  # position for text.
        surface.blit(text, textRect)  # print out the text.
        surface.blit(text2, textRect2)  # print out the text.
        surface.blit(text4, textRect4)  # print out the text.

        text3 = font3.render("Spots Left:" + str(len(self._state._spots)), True, blue)   # tell user spots remaining.
        textRect3 = text3.get_rect()
        textRect3.center = (82, 13)         # set center of this text.
        surface.blit(text3, textRect3)
        if self.level == 15:            # check game level.
            if len(self._state._spots) == 0:
                self._close()

    def _resize_surface(self, size: (int, int)) -> None:
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def _on_mouse_button(self, pos: (int, int)) -> None:
        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()
        pixel_x, pixel_y = pos
        frac_x = pixel_x / width
        frac_y = pixel_y / height

        self._state.handle_click((frac_x, frac_y))

    def _move_spots(self) -> None:
        self._state.move_all_spots()
        self._check()

    def _check(self):
        if len(self._state._spots) == 0 and self.d == 'Level One':  # check game level.
            self.level = 15  # number of ball
            self.d = "Level Two"  # change game level.
            self.run()
            self._fillcolor()
        if self.level == 15:  # check if its in level two.
            if len(self._state._spots) == 0:
                self.d = 'CONGRATULATION!!!'
                self.c = "Click here                to exit."  # tell the user how to exit.
                self.rule = "You Win."  # tell user game end.

    def _close(self):
        myimage = pygame.image.load('x.png')  # load the image
        surface = pygame.display.get_surface()
        surface.blit(myimage, [265, 350])  # draw the image at this place
        pygame.display.flip()
        while True:
            for event in pygame.event.get():  # get event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 265 <= event.pos[0] <= 365 and 350 <= event.pos[1] <= 450:  # decide if the click is ok.
                        pygame.quit()  # quit the game.
                        sys.exit()  # quit the system.


if __name__ == '__main__':
    SpotsGame().run()  # begin the program.
