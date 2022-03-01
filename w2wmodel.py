# coding: utf-8

import re
import time
import random
import argparse
import numpy as np

def find_closest(word, singlish_dict, english_dict, english_arr):
    if word not in singlish_dict.keys():
        return "<OOV>"
    else:
        List2 = singlish_dict[word]
        sims = english_arr.dot(List2)/ (np.linalg.norm(english_arr, axis=1) * np.linalg.norm(List2))
        max_index = np.argmax(sims)
    return list(english_dict.keys())[max_index]

def convert_float(lst):
    output = np.array([float(x) for x in lst])
    return output

def special_split(lst):
    lst = lst.split()
    return ' '.join(lst[:-300]), lst[-300:]

def translate_sent(sent, singlish_dict, english_dict, english_arr):
    line_split = sent.split()
    new_line = ""
    for word in line_split:
        new_line += find_closest(word, singlish_dict, english_dict, english_arr) + " "
    return new_line


def main():
    parser = argparse.ArgumentParser(description = "What to clean?")
    parser.add_argument('--sing', type = str, help = "Name of sing file")
    parser.add_argument('--eng', type = str, help = "Name of eng file")
    parser.add_argument('--output_file', type = str, help = "Name of output file")
    parser.add_argument('--num_words', type = int, help = "Number of Singlish/English words to consider")
    parser.add_argument('--test_file', type = str, help = "Name of test file")
    
    args = parser.parse_args()


    file1 = open(args.sing, encoding = "utf-8")
    file2 = open(args.eng, encoding = "utf-8")

    singlish_dict = {}
    english_dict = {}
    first_line = file1.readline()
    first_line = file2.readline()
    english_arr = np.zeros((args.num_words, int(first_line.split()[1])))

    print("Processing datasets")
    for i in range(args.num_words):
        line = file1.readline()
        p1, p2 = special_split(line)
        singlish_dict[p1] = convert_float(p2)


        line = file2.readline()
        p1, p2 = special_split(line)
        english_dict[p1] = convert_float(p2)
        english_arr[i] = convert_float(p2)

    test = open(args.test_file, encoding = "utf-8")
    content = test.read().splitlines()


    print("Translating sentences")
    output = open(args.output_file, "w", encoding = "utf-8")
    completed = 0
    for line in content:
        output.write(translate_sent(line, singlish_dict, english_dict, english_arr) + "\n")
        completed += 1
        if completed % 10 == 0:
            print(completed * 100 / len(content), "completed!")


    
   
if __name__ == '__main__':
    main()

    
