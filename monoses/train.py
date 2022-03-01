# Copyright (C) 2018-2020  Mikel Artetxe <artetxem@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import glob
import gzip
import os
import shutil
import subprocess
import tempfile
from shlex import quote


ROOT = os.path.dirname(os.path.abspath(__file__))
THIRD_PARTY = os.path.abspath(os.environ['MONOSES_THIRD_PARTY']) if 'MONOSES_THIRD_PARTY' in os.environ else ROOT + '/third-party'
PHRASE2VEC = THIRD_PARTY + '/phrase2vec/word2vec'
TRAINING = ROOT + '/training'


def bash(command):
    subprocess.run(['bash', '-c', command])



# Step 3: Train embeddings
# Step 3: Train embeddings
def train_embeddings(args):
    root = "./../embeddings"
    for part in ('src', 'trg'):
        corpus = './../data/datasets/processed/small_cleaned_corpus.' + part

        # Extract n-grams
        counts = []
        for i, cutoff in enumerate(args.vocab_cutoff):
            counts.append(quote(args.tmp + '/ngrams.' + str(i+1)))
            bash('python3 ' + quote(TRAINING + '/extract-ngrams.py') +
                 ' -i ' + quote(corpus) +
                 ' --min-order ' + str(i+1) +
                 ' --max-order ' + str(i+1) +
                 ' --min-count ' + str(args.vocab_min_count) +
                 ' | sort -nr' +
                 ' | head -' + str(cutoff) +
                 ' > ' + counts[-1])
        bash('cat ' + ' '.join(counts) + ' | cut -f2 > ' + quote(args.tmp + '/phrases.txt'))

        # Build standard word2vec vocabulary
        bash(quote(PHRASE2VEC) +
             ' -train ' + quote(corpus) +
             ' -min-count ' + str(args.vocab_min_count) +
             ' -save-vocab ' + quote(args.tmp + '/vocab-full.txt'))
        bash('head -' + str(args.vocab_cutoff[0]) +
             ' ' + quote(args.tmp + '/vocab-full.txt') +
             ' > ' + quote(args.tmp + '/vocab.txt'))

        # Train embeddings
        bash(quote(PHRASE2VEC) +
            ' -train ' + quote(corpus) +
            ' -read-vocab ' + quote(args.tmp + '/vocab.txt') +
            ' -phrases ' + quote(args.tmp + '/phrases.txt') +
            ' -cbow 0 -hs 0 -sample 0' +  # Fixed params
            ' -size ' + str(args.emb_size) +
            ' -window ' + str(args.emb_window) + 
            ' -negative ' + str(args.emb_negative) +
            ' -iter ' + str(args.emb_iter) +
            ' -threads ' + str(args.threads) +
            ' -output ' + quote(root + '/emb.' + part))

        # Clean temporary files
        for f in os.listdir(args.tmp):
            os.remove(os.path.join(args.tmp, f))



def main():
    parser = argparse.ArgumentParser(description='Train an unsupervised SMT model')
    parser.add_argument('--threads', metavar='N', type=int, default=20, help='Number of threads (defaults to 20)')

    phrase2vec_group = parser.add_argument_group('Step 3', 'Phrase embedding training')
    phrase2vec_group.add_argument('--vocab-cutoff', metavar='N', type=int, nargs='+', default=[200000, 400000, 400000], help='Vocabulary cut-off (defaults to 200000 400000 400000)')
    phrase2vec_group.add_argument('--vocab-min-count', metavar='N', type=int, default=10, help='Discard words with less than N occurrences (defaults to 10)')
    phrase2vec_group.add_argument('--emb-size', metavar='N', type=int, default=300, help='Dimensionality of the phrase embeddings (defaults to 300)')
    phrase2vec_group.add_argument('--emb-window', metavar='N', type=int, default=5, help='Max skip length between words (defauls to 5)')
    phrase2vec_group.add_argument('--emb-negative', metavar='N', type=int, default=10, help='Number of negative examples (defaults to 10)')
    phrase2vec_group.add_argument('--emb-iter', metavar='N', type=int, default=5, help='Number of training epochs (defaults to 5)')

    args = parser.parse_args()

    args.tmp = "temp"

    os.makedirs("temp", exist_ok=True)
    os.makedirs(args.tmp, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.tmp) as args.tmp:
        train_embeddings(args)

if __name__ == '__main__':
    main()
