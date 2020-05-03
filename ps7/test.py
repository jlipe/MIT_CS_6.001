import random

def monteHall(numSims):
    doors = [0,0,1]
    correct_plays_no_switch = 0.0
    correct_plays_switch = 0.0
    for n in range(numSims):
        choice_index = random.randint(0, 2)
        first_choice_number = doors[choice_index]
        remaining_doors = doors[:]
        del remaining_doors[choice_index]
        if 1 in remaining_doors:
            possible_switch_door = 1
        else:
            possible_switch_door = 0

        if first_choice_number == 1:
            correct_plays_no_switch += 1
        elif possible_switch_door == 1:
            correct_plays_switch += 1

    return (correct_plays_no_switch / numSims, correct_plays_switch / numSims)


print monteHall(10000)
