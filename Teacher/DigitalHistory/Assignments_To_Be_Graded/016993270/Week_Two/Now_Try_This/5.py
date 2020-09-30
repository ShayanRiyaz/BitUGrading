# Please note that if you uncomment and press multiple times, the program will keep appending to the file.

def cap_four(name):
    new_name = name[0].upper() + name[1:3] + name[3].upper() + name[4:]
    return new_name

# Check
answer = cap_four('macdonald')
print(answer)