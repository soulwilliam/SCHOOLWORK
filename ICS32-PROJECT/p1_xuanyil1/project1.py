'''This project take an positive integer as input
and make a downward block diagonal of size of the same number
'''

#Take input and calculate the num of three plus.
n = int(input())
num_three_should_be = n - 1
num_three_right_now = 0

#Setup all string that need to be drawn
two_plus = '+-+'
middle = '| |'
three_plus = '+-+-+'
indent = '  '

#Draw the downward block with correct indent and length
print(two_plus)
for i in range(n):
    print(middle)
    if num_three_right_now < num_three_should_be:
        print(three_plus)
    else:
        print(two_plus)
    num_three_right_now += 1
    middle = indent + middle
    three_plus = indent + three_plus
    two_plus = indent + two_plus
