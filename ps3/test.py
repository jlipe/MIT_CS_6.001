def isPalindromeRec(sentence):
    if len(sentence) <= 1:
        return True
    else:
        return sentence[0] == sentence[-1] and isPalindromeRec(sentence[1:-1])

def isPalindromeLin(sentence):
    midpoint = len(sentence) / 2.0
    if midpoint % 1 != 0:
        lower_check = int(midpoint - 0.5)
        upper_check = int(midpoint + 0.5)
        return sentence[:lower_check][::-1] == sentence[upper_check:]
    else:
        return sentence[:int(midpoint)][::-1] == sentence[int(midpoint):]



print isPalindromeLin("agoiheapoiehpgoiha")
print isPalindromeRec("gahpoeighaopieghaigaepoihgapoeihgpoaeihpodcapoibgiophepgapoihpaoeighopeag")
