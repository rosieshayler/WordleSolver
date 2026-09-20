with open("wordlewords.txt") as f:
    wordle_words = [line.strip() for line in f]
#alphabet = list(string.ascii_lowercase)

score = "00000"
green_letters = ["","","","",""]
possible_words = wordle_words
count = 0

import copy 
while (score!="22222"):
    count += 1
    #finding what was entered
    validation = False
    while not validation:
        word_tried = input("Input: ").lower()
        if len(word_tried)==5:
            validation = True
    validation = False
    while not validation:
        score = input("Output: ")
        if len(score)==5:
            validation = True
            for x in range(5):
                if score[x]!='0' and score[x]!='1' and score[x]!='2':
                    validation = False
    
    if score == 22222:
        break

    letter_counts = {}
    for char in word_tried:
        if char not in letter_counts:
            letter_counts[char] = {'min': 0, 'max': 5, 'banned_positions': []}

    for x in range(5):
        letter = word_tried[x]
        status = score[x]
    
        if status == '2':
            green_letters[x] = letter
            letter_counts[letter]['min'] += 1
        elif status == '1':
            letter_counts[letter]['min'] +=1
            letter_counts[letter]['banned_positions'].append(x)
        
    for x in range(5):
        letter = word_tried[x]
        status = score[x]

        if status == '0':
            letter_counts[letter]['max'] = letter_counts[letter]['min']
            letter_counts[letter]['banned_positions'].append(x)

    print("Here is a list of all possible words to try next: ")
    #find a list of new possible words
    new_possible_words = []
    for word in possible_words:
        valid_word = True

        #green letters
        for x in range(5):
            if green_letters[x] != '' and green_letters[x] != word[x]:
                valid_word = False
                break 

        # skip to next word        
        if not valid_word:
            continue
        
        #banned positions 
        for x in range(5):
            char = word[x]

            if char in letter_counts and x in letter_counts[char]['banned_positions']:
                valid_word = False
                break

        if not valid_word:
            continue

        #frequencues 
        word_counts = {}
        for char in word:
            word_counts[char] = word_counts.get(char, 0) + 1
        
        for char, constraints in letter_counts.items():
            actual_count = word_counts.get(char, 0)
            if actual_count < constraints['min'] or actual_count > constraints['max']:
                valid_word = False
                break
        
        if not valid_word:
            continue

        new_possible_words.append(word)
        print(word)
    
    possible_words = new_possible_words

print('Well done, you have solved this wordle in ', count, ' attempts! Correct answer: ', word_tried)
