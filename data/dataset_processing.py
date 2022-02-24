# coding: utf-8

import re
import time
import random
import argparse



def read_as_dic(fname):
    file = open("data_processing/"+fname)
    content = file.read().splitlines()
    dic = {}
    for line in content:
        line = line.split(",")
        dic[line[0]] = line[1]
    return dic

def read_as_lst(fname):
    file = open("data_processing/"+fname)
    content = file.read().splitlines()
    return content

def special_replace(og_word, new_word, line):
    new_line = line
    if new_line[:len(og_word)+1] == og_word + " " or new_line[-3-len(og_word):-2] == " " + og_word:
        new_line = re.sub(og_word, new_word, new_line)
    return re.sub(" " + og_word + " ", " " + new_word + " ",new_line)

def tokenizer(line):
    line = line.lower()
    line = line.replace("\'", " &apos;")
    line = line.replace("\’", " &apos;")
    line = line.replace("."," .")
    line = line.replace("?"," ?")
    line = line.replace("!", "!")
    return line

clean_english_replace = read_as_dic("clean_english_replace.txt")
clean_english_regex = read_as_dic("clean_english_regex.txt")
clean_singlish_replace = read_as_dic("clean_singlish_replace.txt")
clean_singlish_regex = read_as_dic("clean_singlish_regex.txt")
clean_english_to_singlish = read_as_dic("clean_english_to_singlish.txt")
singlish_vocab = read_as_lst("singlish_vocab.txt")


def cleaning(input_file, output_file, lower, tokenize, clean_text, english_to_singlish, filtering):

    print("lower", lower)
    print("tokenize", tokenize)
    print("clean text", clean_text)
    print("english_to_singlish", english_to_singlish)
    print("filtering", filtering)

    start = time.time()

    my_file = open(input_file, encoding = "utf-8")
    content = my_file.readlines()

    if filtering == True:
        kept = open(output_file, "w", encoding = "utf-8")
        discard = open(output_file + ".out", "w", encoding = "utf-8")
    else:
        output_file = open(output_file,"w", encoding = "utf-8")
        
    
    i = 0
    for line in content:

        original_line = line

        if lower:
            line = line.lower()
        
        if clean_text:
        # Clean English words/phrases
            for word in clean_english_replace.keys():
                line = special_replace(word, clean_english_replace[word],line)
            for word in clean_english_regex.keys():
                line = re.sub(word, clean_english_regex[word],line)
            for word in clean_singlish_replace.keys():
                line = special_replace(word, clean_singlish_replace[word],line)
            for word in clean_singlish_regex.keys():
                line = re.sub(word, clean_singlish_regex[word],line)


        if english_to_singlish:
            # Convert English to Singlish
            for word in clean_english_to_singlish.keys():
                line = special_replace(word, clean_english_to_singlish[word],line)

        if filtering:
            # Filtering
            for word in singlish_vocab:
                if word in line:
                    if tokenize:
                        line = tokenizer(line)
                    kept.write(line)
                    break
                else:
                    if word == singlish_vocab[-1]:
                        discard.write(line)
        else:
            if tokenize:
                line = tokenizer(line)
            output_file.write(line)
            

        i += 1
        if i % 100000 == 0:
            print(i*100 / len(content), "% done")

    
    print("Time taken", time.time() - start)

def main():
    parser = argparse.ArgumentParser(description = "What to clean?")
    parser.add_argument('--input_file', type = str, help = "Name of input file")
    parser.add_argument('--output_file', type = str, help = "Name of output file")
    parser.add_argument('--lower', action = 'store_true', help = "Convert to lower")
    parser.add_argument('--tokenize', action = 'store_true', help = "Tokenize text")
    parser.add_argument('--clean_text', action='store_true', help = "Clean Text")
    parser.add_argument('--english_to_singlish', action='store_true', help = "Convert English to Singish")
    parser.add_argument('--filtering', action='store_true', help = "Filter")
    
    args = parser.parse_args()
    cleaning(args.input_file, args.output_file, args.lower, args.tokenize, args.clean_text, args.english_to_singlish, args.filtering)
    
    print("Processing complete!")
    
   
if __name__ == '__main__':
    main()
    
