# Write code below 💖

while True:
    try: 
        earthWeight = float(input('\nWhat is your weight in kg? '))
        break
    except ValueError:
        print('Please write a real number\n')

print("\nPlanet        Number")
print("Mercury         1")
print("Venus           2")
print("Mars            3")
print("Jupiter         4")
print("Saturn          5")
print("Uranus          6")
print("Neptune         7")

while True:
  planetDestiny = input('\nWhat is the number of planet of desiny? ')
  if planetDestiny == '1':
    print('Your weight in Mercury will be', earthWeight * 0.38)
    print('')
    break
  elif planetDestiny == '2':
    print('Your weight in Venus will be', earthWeight * 0.91)
    print('')
    break
  elif planetDestiny == '3':
    print('Your weight in Mars will be', earthWeight * 0.38)
    print('')
    break
  elif planetDestiny == '4':
    print('Your weight in Jupiter will be', earthWeight * 2.53)
    print('')
    break
  elif planetDestiny == '5':
    print('Your weight in Saturn will be', earthWeight * 1.07)
    print('')
    break
  elif planetDestiny == '6':
    print('Your weight in Uranus will be', earthWeight * 0.89)
    print('')
    break
  elif planetDestiny == '7':
    print('Your weight in Neptune will be', earthWeight * 1.14)
    print('')
    break
  else:
    print('Invalid planet number, try again')