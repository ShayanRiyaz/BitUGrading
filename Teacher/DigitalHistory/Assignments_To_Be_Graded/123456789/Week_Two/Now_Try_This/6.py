# Please note that if you uncomment and press multiple times, the program will keep appending to the file.

x = 5
y = 0
try:
    z = x/y
except ZeroDivisionError:
    print("Can't divide by Zero!")
finally:
    print('All Done!')