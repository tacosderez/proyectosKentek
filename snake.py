import random

WIDTH = 30
HEIGHT = 10
INFINITE = False


snake = [[1,5],[2,5],[3,5], [4,5], [5,5]]
pos = [5,5]
length = 5
score = 0
food = [random.randrange(0,WIDTH), random.randrange(0,HEIGHT)]
last_dir = 'd' 

moves = 0
# Main loop
while True:
    score_string = "Score: "+ str(score)+" "
    moves_string = "Moves: "+ str(moves)
    print(score_string + (" "*(WIDTH+2 - len(score_string)- len(moves_string))) + moves_string)
    print("╔"+("═"*WIDTH)+"╗")
    # Render Field
    for y in range(HEIGHT):
        print("║", end="")
        for x in range(WIDTH):
            if [x, y] == pos:
                print("■", end="")
            elif [x, y] in snake:
                print("█", end="")
            elif [x,y] == food:
                print('©', end="")
            else:
                print(" ", end="")
        print("║")
    print("╚"+("═"*WIDTH)+"╝")
    
    

    # Process movement
    try:
        dir = input()[0]
    except:
        print("invvalid move")
        continue

    if dir == 'w' and last_dir != "s":
        pos[1] -= 1
    elif dir == "a" and last_dir != "d":
        pos[0] -= 1
    elif dir == 's' and last_dir != "w":
        pos[1] += 1
    elif dir == "d" and last_dir != "a":
        pos[0] += 1
    else:
        print("invalid move")
        continue
    last_dir = dir

    # Process Walls
    if INFINITE:
        if pos[0] >= WIDTH:
            pos[0] = 0
        if pos [0] < 0:
            pos[0] = WIDTH - 1
        if pos[1] >= HEIGHT:
            pos[1] = 0
        if pos [1] < 0:
            pos[1] = HEIGHT - 1
    else:
        if pos[0] >= WIDTH:
            break
        if pos [0] < 0:
            break
        if pos[1] >= HEIGHT:
            break
        if pos [1] < 0:
            break
    
    #Moves counter
    moves= moves +1

    # Process food
    if pos == food:
        food = [random.randrange(0,WIDTH), random.randrange(0,HEIGHT)]
        while food in snake and food != pos:
            food = [random.randrange(0,WIDTH), random.randrange(0,HEIGHT)]
        length += 1
        score +=1

    # Keep snake at length
    while len(snake) > length:
        snake.pop(0)

    #When die
    if pos in snake:
        break
    snake.append([pos[0], pos[1]])

    #Spacer/buffer

    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

print("You lost")
print("Score:", score)

