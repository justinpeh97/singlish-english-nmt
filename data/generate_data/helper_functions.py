
import time
import re



def clean_comments_hwz(comments):
    cleaned_comments = []
    for comment in comments:
        comment = comment[:-1]
        while "Click to expand..." in comment:
            pos = re.search("Click to expand....",comment)
            comment = comment[(pos.span()[1]):]
        if "Sent from" in comment:
            pos = re.search("Sent from",comment)
            comment = comment[:(pos.span()[0])]
        if "Posted from" in comment:
            pos = re.search("Posted from",comment)
            comment = comment[:(pos.span()[0])]
        if re.search(u'[\u4e00-\u9fff]', comment):
            continue
        if "lightbox_close" in comment:
            continue
        if "www." in comment or "http" in comment or ".com" in comment:
            continue
        if len(comment) > 100000:
            continue

        cleaned_comments.append(comment)

    return cleaned_comments

def clean_comments_reddit(comments):
    clean_comments = []
    for comment in comments:
        comment = re.sub('[\n|\t]+',"",comment)
        comment = comment.lower()
        comment = re.sub("[~`^*{}<>|\[\]]", "", comment)
        comment = re.sub("edit:", "", comment)
        if "www." in comment or "http" in comment or ".com" in comment:
            continue
        clean_comments.append(comment)
    return clean_comments
    

def custom_splitting(comments,symbol):
    output = []
    for comment in comments:
        if symbol in comment:
            comment_split = comment.split(symbol)
            for index in range(len(comment_split)-1):
                comment_split[index] += symbol
            output.extend(comment_split)
        else:
            output.append(comment)
    return output

def convert_to_sentences(comments):
    all_sentences = custom_splitting(comments, ".") # Split by "."
    all_sentences = custom_splitting(all_sentences, "!") # Split by "!"
    all_sentences = custom_splitting(all_sentences, "?") # Split by "?"
    return all_sentences

def percentage_alphabets(sentence):
    len_sent = len(sentence)
    num_alpha = 0
    for char in sentence:
        if char.isalpha() or char == " ":
            num_alpha += 1
    return num_alpha / len_sent

def filter_sentences(sentences):
    sentences_kept = []
    for sentence in sentences:
        if len(sentence) <= 15 or len(sentence.split()) < 3 or percentage_alphabets(sentence) < 0.75 or len(sentence) > 500:
            continue
        if sentence[0] == " ":
            sentence = sentence[1:]
        sentences_kept.append(sentence)
    return sentences_kept



