def findAll(wordlist, lStr):
    return_list = []
    for word in wordlist.split(" "):
        possible_word = ""
        for l in word:
            if l not in possible_word and l in lStr:
                possible_word += l
        if possible_word == word:
            return_list.append(word)
    return return_list

print findAll("hello goodbye hi no not here", 'hinoter')
