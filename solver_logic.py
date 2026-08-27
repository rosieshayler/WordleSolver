def load_words(filepath="wordlewords.txt"):
    """Reads the text file and returns a list of lowercase words."""
    try:
        with open(filepath) as f:
            return [line.strip().lower() for line in f]
    except FileNotFoundError:
        return []

def filter_wordle_words(possible_words, word_tried, score):
    """
    Takes the current list of possible words, the word just tried, and the 
    score of that word (0 = grey, 1 = yellow, 2 = green) and returns a list 
    of all remaining possible words.
    """
    word_tried = word_tried.lower()
    new_possible_words = []

    #initilise for this specific guess
    letter_counts = {}
    for char in word_tried:
        if char not in letter_counts:
            letter_counts[char] = {'min': 0, 'max': 5, 'banned_positions': []}

    green_letters = ["", "", "", "", ""]

    #establish minimum amount of times this letter can be in the word, using yellows and greens
    for x in range(5):
        letter = word_tried[x]
        status = score[x]
    
        if status == '2':
            green_letters[x] = letter
            letter_counts[letter]['min'] += 1
        elif status == '1':
            letter_counts[letter]['min'] +=1
            letter_counts[letter]['banned_positions'].append(x)
    
    #establish maximum times this letter is in the word, using greys 
    for x in range(5):
        letter = word_tried[x]
        status = score[x]

        if status == '0':
            letter_counts[letter]['max'] = letter_counts[letter]['min']
            letter_counts[letter]['banned_positions'].append(x)

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

        # skip to next word
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
    
    return new_possible_words