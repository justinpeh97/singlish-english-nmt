
my_file = open("./../full_singlish_lower.txt", encoding = "utf-8")
content = my_file.readlines()

print("Read file")

word_counts = {}

for line in content:
    line_split = line.split()
    for word in line_split:
        if word in word_counts.keys():
            word_counts[word] += 1
        else:
            word_counts[word] = 1



print("Sorting")

sorted_counts = sorted(word_counts.items(), key = lambda x:x[1], reverse = True)

file = open("most_common_words.txt",'w', encoding = 'utf8')
for word in sorted_counts:
    file.write(word[0] + " " + str(word[1]) + " "  + "\n")
