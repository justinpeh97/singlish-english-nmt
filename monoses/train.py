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
FAST_ALIGN = THIRD_PARTY + '/fast_align/build'
MOSES = THIRD_PARTY + '/moses'
FAIRSEQ = THIRD_PARTY + '/fairseq'
VECMAP = THIRD_PARTY + '/vecmap'
SUBWORD_NMT = THIRD_PARTY + '/subword-nmt'
PHRASE2VEC = THIRD_PARTY + '/phrase2vec/word2vec'
TRAINING = ROOT + '/training'


def bash(command):
    subprocess.run(['bash', '-c', command])


def count_lines(path):
    return int(subprocess.run(['wc', '-l', path], stdout=subprocess.PIPE).stdout.decode('utf-8').strip().split()[0])


def binarize(output_config, output_pt, lm_path, lm_order, phrase_table, reordering=None, pt_scores=4, prune=100):
    output_pt = os.path.abspath(output_pt)
    lm_path = os.path.abspath(lm_path)

    # Binarize
    reord_args = ' --lex-ro ' + quote(reordering) + ' --num-lex-scores 6' if reordering is not None else ''
    bash(quote(MOSES + '/scripts/generic/binarize4moses2.perl') +
         ' --phrase-table ' + quote(phrase_table) +
         ' --output-dir ' + quote(output_pt) +
         ' --num-scores ' + str(pt_scores) +
         ' --prune ' + str(prune) +
         reord_args)

    # Clean temporary files created by the binarization script
    for tmp in glob.glob(output_pt + '/../tmp.*'):
        shutil.rmtree(tmp)

    # Build configuration file
    with open(output_config, 'w') as f:
        print('[input-factors]', file=f)
        print('0', file=f)
        print('', file=f)
        print('[mapping]', file=f)
        print('0 T 0', file=f)
        print('', file=f)
        print('[distortion-limit]', file=f)
        print('6', file=f)
        print('', file=f)
        print('[feature]', file=f)
        print('UnknownWordPenalty', file=f)
        print('WordPenalty', file=f)
        print('PhrasePenalty', file=f)
        print('ProbingPT name=TranslationModel0 num-features=' + str(pt_scores) +
              ' path=' + output_pt + ' input-factor=0 output-factor=0', file=f)
        if reordering is not None:
            print('LexicalReordering name=LexicalReordering0' +
                  ' num-features=6 type=wbe-msd-bidirectional-fe-allff' +
                  ' input-factor=0 output-factor=0 property-index=0', file=f)
        print('Distortion', file=f)
        print('KENLM name=LM0 factor=0 path=' + lm_path +
              ' order=' + str(lm_order), file=f)
        print('', file=f)
        print('[weight]', file=f)
        print('UnknownWordPenalty0= 1', file=f)
        print('WordPenalty0= -1', file=f)
        print('PhrasePenalty0= 0.2', file=f)
        print('TranslationModel0=' + (' 0.2'*pt_scores), file=f)
        if reordering is not None:
            print('LexicalReordering0= 0.3 0.3 0.3 0.3 0.3 0.3', file=f)
        print('Distortion0= 0.3', file=f)
        print('LM0= 0.5', file=f)




# Step 3: Train embeddings
def train_embeddings(args):
    root = ./../embeddings
    os.mkdir(root)
    for part in ('src', 'trg'):
        corpus = './../data/datasets/processed/cleaned_corpus.' + part

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
    parser.add_argument('--working', metavar='PATH', required=True, help='Working directory')
    parser.add_argument('--tmp', metavar='PATH', help='Temporary directory')
    parser.add_argument('--threads', metavar='N', type=int, default=20, help='Number of threads (defaults to 20)')

    parser.add_argument('--pt-prune', metavar='N', type=int, default=100, help='Phrase-table pruning (defaults to 100)')  # TODO Which group?
    parser.add_argument('--cube-pruning-pop-limit', metavar='N', type=int, default=1000, help='Cube pruning pop limit for fast decoding (defaults to 1000)')  # TODO Which group?



    phrase2vec_group = parser.add_argument_group('Step 3', 'Phrase embedding training')
    phrase2vec_group.add_argument('--vocab-cutoff', metavar='N', type=int, nargs='+', default=[200000, 400000, 400000], help='Vocabulary cut-off (defaults to 200000 400000 400000)')
    phrase2vec_group.add_argument('--vocab-min-count', metavar='N', type=int, default=10, help='Discard words with less than N occurrences (defaults to 10)')
    phrase2vec_group.add_argument('--emb-size', metavar='N', type=int, default=300, help='Dimensionality of the phrase embeddings (defaults to 300)')
    phrase2vec_group.add_argument('--emb-window', metavar='N', type=int, default=5, help='Max skip length between words (defauls to 5)')
    phrase2vec_group.add_argument('--emb-negative', metavar='N', type=int, default=10, help='Number of negative examples (defaults to 10)')
    phrase2vec_group.add_argument('--emb-iter', metavar='N', type=int, default=5, help='Number of training epochs (defaults to 5)')


    args = parser.parse_args()

    if args.tmp is None:
        args.tmp = args.working

    os.makedirs(args.working, exist_ok=True)
    os.makedirs(args.tmp, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.tmp) as args.tmp:
        train_embeddings(args)


if __name__ == '__main__':
    main()
