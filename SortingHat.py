# The Sorting Hat
Gryffindor = 0
Ravenclaw = 0
Hufflepuff = 0
Slytherin = 0

# Question 1 process
while True:
  Q1 = input('Do you like Dawn or Dusk? \n 1) Dawn \n 2) Dusk \nEnter 1-2 \n')
  
  if Q1 =="1":
    Gryffindor +=1
    Ravenclaw +=1
    break
  elif Q1 =="2":
    Hufflepuff +=1
    Slytherin +=1
    break
  else:
    print('wrong input, try again')
print(chr(27) + "[2J")

# Question 2 process
while True:
  Q2 = input("When I'm dead, I want people to remember me as:\n 1) The Good \n 2) The Great \n 3) The Wise \n 4) The Bold \nEnter 1-4 \n")
  
  if Q2 =="1":
    Hufflepuff += 1
    break
  elif Q2 =="2":
    Gryffindor +=1
    break
  elif Q2 =="3":
    Ravenclaw += 1
    break
  elif Q2 =="4":
    Slytherin +=1
    break
  else:
    print('Wrong input, try again')
print(chr(27) + "[2J")

# Question 3 process
while True:
  Q3 = input('Which kind of instrument most pleases your ear? \n 1) The violin \n 2) The trumpet \n 3) The piano \n 4) The drum \nEnter 1-4 \n' )
  if Q3 =="1":
    Hufflepuff += 1
    break
  elif Q3 =="2":
    Gryffindor +=1
    break
  elif Q3 =="3":
    Ravenclaw += 1
    break
  elif Q3 =="4":
    Slytherin +=1
    break
  else:
    print('Wrong input, try again')
print(chr(27) + "[2J")

# Question 4 process
while True:
  Q4 = input('What is your favorite class? \n 1) Herbology/Beastiology \n 2) Defense Against the Dark Arts \n 3) Charms \n 4) Potions \nEnter 1-4 \n')
  if Q4 =="1":
    Hufflepuff += 1
    break
  elif Q4 =="2":
    Gryffindor +=1
    break
  elif Q4 =="3":
    Ravenclaw += 1
    break
  elif Q4 =="4":
    Slytherin +=1
    break
  else:
    print('Wrong input, try again')
print(chr(27) + "[2J")

# Question 5 process
while True:
  Q5 = input('Where would you go in your free time \n 1) Enter the forbidden forest \n 2) Get a Butterbeer \n 3) Hit the library \n 4) Play pranks on my classmates \nEnter 1-4 \n')
  if Q5 =="1":
    Hufflepuff += 1
    break
  elif Q5 =="2":
    Gryffindor +=1
    break
  elif Q5 =="3":
    Ravenclaw += 1
    break
  elif Q5 =="4":
    Slytherin +=1
    break
  else:
    print('Wrong input, try again')
print(chr(27) + "[2J")

# Question 6 process
while True:
  Q6 = input('What is your favorite magical beast \n 1) Basilisk \n 2) Unicorn \n 3) Phoenix \n 4) Dragon \nEnter 1-4 \n')
  if Q6 =="1":
    Slytherin += 1
    break
  elif Q6 =="2":
    Hufflepuff +=1
    break
  elif Q6 =="3":
    Ravenclaw += 1
    break
  elif Q6 =="4":
    Gryffindor +=1
    break
  else:
    print('Wrong input, try again')
print(chr(27) + "[2J")

# Question 7 process
while True:
  Q7 = input('If you saw a student crying because of a bad grade, what would you do? \n 1) Give them some encouraging words \n 2) Help them study \n 3) Ignore them \n 4) Help them fight for a better grade \nEnter 1-4 \n')
  if Q7 =="1":
    Hufflepuff += 1
    Slytherin -=1
    break
  elif Q7 =="2":
    Ravenclaw +=1
    Hufflepuff -=1
    break
  elif Q7 =="3":
    Slytherin += 1
    Gryffindor -= 1
    break
  elif Q7 =="4":
    Gryffindor +=1
    Ravenclaw -=1
    break
  else:
    print('Wrong input, try again')
print(chr(27) + "[2J")

# Question 8 process
while True:
  Q8 = input('Who is your favorite teacher? \n 1) Prof. Snape \n 2) Prof. McGonnagle \n 3) Hagrid \n 4) Prof. Flitwick \nEnter 1-4 \n')
  if Q8 =="1":
    Slytherin += 1
    break
  elif Q7 =="2":
    Gryffindor +=1
    break
  elif Q8 =="3":
    Hufflepuff += 1
    break
  elif Q8 =="4":
    Ravenclaw +=1
    break
  else:
    print('Wrong input, try again')
print(chr(27) + "[2J")

# Most points

most_points = max(Gryffindor, Ravenclaw, Hufflepuff, Slytherin)

#If there is a tie

if Gryffindor == Ravenclaw and Gryffindor == most_points:
  while True:
    Q9 = input('When faced with a problem, how long do you think before acting \n 1) 1-5 minute \n 2) 5+ minutes \nEnter 1-2 \n')
    if Q9 == "1":
        Gryffindor += 1
        break
    elif Q9 == '2':
        Ravenclaw +=1
        break
    else:
        print('Wrong input, try again')

if Gryffindor == Slytherin and Gryffindor == most_points:
  while True:
    Q9 = input('If you find a stolen item, do you return it? \n 1) Yes \n 2) No \nEnter 1-2 \n')
    if Q9 == "1":
        Gryffindor += 1
        break
    elif Q9 == '2':
        Slytherin +=1
        break
    else:
        print('Wrong input, try again')

if Gryffindor == Hufflepuff and Gryffindor == most_points:
  while True:
    Q9 = input('Do you like adventure? \n 1) Yes \n 2) No \nEnter 1-2 \n')
    if Q9 == "1":
        Gryffindor += 1
        break
    elif Q9 == '2':
        Slytherin +=1
        break
    else:
        print('Wrong input, try again')

if Ravenclaw == Slytherin and Ravenclaw == most_points:
  while True:
    Q9 = input('Would you cheat on an exam? \n 1) Yes \n 2) No \nEnter 1-2 \n')
    if Q9 == "1":
        Slytherin += 1
        break
    elif Q9 == '2':
        Ravenclaw +=1
        break
    else:
        print('Wrong input, try again')

if Ravenclaw == Hufflepuff and Ravenclaw == most_points:
  while True:
    Q9 = input('Do you prefer to spend time with your friends or studying? \n 1) Friends \n 2) Studying \nEnter 1-2')
    if Q9 == "1":
        Hufflepuff += 1
        break
    elif Q9 == '2':
        Ravenclaw +=1
        break
    else:
        print('Wrong input, try again')

if Hufflepuff == Slytherin and Hufflepuff == most_points:
  while True:
    Q9 = input("What do you think of magical beasts? \n 1) They are the best part about the wizarding world \n 2) They're okay \n 3) I hate them \nEnter 1-3")
    if Q9 == "1":
        Hufflepuff += 1
        break
    elif Q9 == '2':
        Slytherin +=1
        break
    elif Q9 == '3':
        Slytherin +=2
        break
    else:
        print('Wrong input, try again')


# Redifine points

most_points = max(Gryffindor, Ravenclaw, Hufflepuff, Slytherin)

# Score tracker

print('Gryffindor: ',Gryffindor)
print('Ravenclaw: ', '',Ravenclaw)
print('Hufflepuff: ',Hufflepuff)
print('Slytherin: ', '',Slytherin) 
print('')

# Winning House

if Gryffindor == most_points:
  print('You are a Gryffindor!!🦁')
elif Ravenclaw == most_points:
  print('You are a Ravenclaw!!🐦‍⬛')
elif Hufflepuff == most_points:
  print('You are a Hufflepuff!!🦡')
else:
  print('You are a Slytherin!!🐍')