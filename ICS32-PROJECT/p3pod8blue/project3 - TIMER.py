'''
Xuanyi Lin                      xuanyil1
Cayson Kai-Sheng Yim            yimck

Project3 cons only
'''

import connectfour as c4
import time
import random

'''
This program renders a two player Connect Four game
with the default dimensions of 7 columns by 6 rows.
In order to win, one must have their drops, either red or yellow,
aligned 4 in a row. Furthermore, our game allows you to
customize the dimensions of the board based on an input your choice.
'''

def main():
    # Set deflaut number for time out
    timeout = 10

    winnercolor = ''

    # Ask if user want customize the board and set the data.
    cus = input('Wanna customize the board?: (Y/N)')
    newC = c4.BOARD_COLUMNS
    if cus == 'Y':
        newC = int(input('Number of columns: '))
        newR = int(input('Number of rows: '))
        c4.BOARD_COLUMNS = newC
        c4.BOARD_ROWS = newR

    # Create the game
    New_game = c4.new_game()
    print('RED represents the first player')
    print()
    print('YELLOW represents the second player')
    print()

    # Keep running if there's no winner or if the board is not full
    while(c4.winner(New_game) == 0):
        n = newC
        if New_game.turn == c4.RED:
            print("RED's turn")
        elif New_game.turn == c4.YELLOW:
            print("YELLOW's turn")

        # Get the time and if exceed 10s no input, it will randomly drop
        t = time.time()
        endt = time.time()+timeout
        prompt = 'Number of column you want to drop(1-{0}): \n'.format(newC)
        col = input(prompt)
        if time.time() > endt:
            print('exceed 10 seconds, randomly drop')
            col = random.randint(0,c4.BOARD_COLUMNS-1) + 1
        col = int(col)
        print(col)
        col = col - 1

        # Drop and update the game with new board and new turn
        New_game = c4.drop(New_game, col)

        # Print the numbers of columns
        for i in range(n):
            g = i+1
            print(str(g) + ' ', end = '')
        print('\n',end = '')
        contdot = 0

        # Draw the board (0 to .; 1 to R; 2 to Y)
        for i in range(len(New_game.board[0])):
            for j in range(len(New_game.board)):
                if New_game.board[j][i] == 0:
                    print('. ', end = '')
                    contdot += 1
                elif New_game.board[j][i] == 1:
                    print('R ', end = '')
                elif New_game.board[j][i] == 2:
                    print('Y ', end = '')
            print('\n', end = '')
        print()

        #if no space for dot, break
        if contdot == 0:
            break
            
    # Set winner and message
    if c4.winner(New_game) == 1:
        winnercolor = 'RED'
    elif c4.winner(New_game) == 2:
        winnercolor = 'YELLOW'
    elif c4.winner(New_game) == 0:
        winnercolor = 'NONE'
    print('Winner is:', winnercolor)


if __name__ == '__main__':
    main()
