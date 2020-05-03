#1.1 prob of three heads = 1/(2^3) = .125
#1.2 prob = .125
#1.3 prob = (3/8) = 0.375
#1.4 prob = 0.5

#2.1 prob = (1/6)^4 = .0007716

import random

#yahtzee code
def yahtzee_rolls(simulations):
    yahtzee = 0
    for j in range(simulations):
        die = [1,2,3,4,5,6]
        dice_rolls = []
        for n in range(5):
            dice_rolls.append(random.choice(die))
        if dice_rolls[0] == dice_rolls[1] == dice_rolls[2] == \
        dice_rolls[3] == dice_rolls[4]:
            yahtzee += 1
    return float(yahtzee) / float(simulations)

print yahtzee_rolls(1000000)
