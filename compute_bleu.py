import re
from nltk.translate.bleu_score import corpus_bleu
from nltk.translate.meteor_score import meteor_score
import os
import argparse


def load_references(file):
    automatic_references_file = open(file, encoding = "utf-8")
    content = automatic_references_file.read().splitlines()
    automatic_references = []
    for line in content:
        line = line.lower()
        line = re.sub(r'[^\w\s]','',line)
        automatic_references.append([line.split()])
    return automatic_references


def compute_bleu(candidates, references):
    bleu_score = round(corpus_bleu(references, candidates) * 100,4)
    print("BLEU score:", bleu_score)
    return bleu_score


def run_scores(file1, file2):
    


    automatic_references = load_references(file1)
    automatic_candidates_file = open(file2, encoding = "utf-8")
    content = automatic_candidates_file.read().splitlines()
    automatic_candidates = []
    for line in content:
        line = re.sub(" &apos;", "", line)
        line = re.sub(r'[^\w\s]','',line)
        automatic_candidates.append(line.split())

    bleu_score = compute_bleu(automatic_candidates, automatic_references)
            

def main():
    parser = argparse.ArgumentParser(description = "What to clean?")
    parser.add_argument('--candidate', type = str, help = "Name of candidate file")
    parser.add_argument('--ref', type = str, help = "Name of reference file")
    
    args = parser.parse_args()

    run_scores(args.candidate, args.ref)

if __name__ == '__main__':
    main()
