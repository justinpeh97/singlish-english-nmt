import re
import time
import random




#my_file = open("./../experimentations/full_singlish_lower.txt", encoding = "utf-8")
my_file = open("./../experimentations/singlish_cleaned_kept_lower.txt", encoding = "utf-8")
content = my_file.readlines()


def check_word(word):

    sentences = []
    occurences = 0
    for line in content:
        if word in line:
            occurences += 1
            sentences.append(line)

    print("Number of occurences - ", word, ":", occurences)

        
    random.shuffle(sentences)
    return sentences[:20]
    
