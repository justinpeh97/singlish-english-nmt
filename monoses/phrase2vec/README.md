Phrase2vec
==============

This is an extension of word2vec to learn n-gram (phrase) embeddings as described in the following paper (Section 3.1):

Mikel Artetxe, Gorka Labaka, and Eneko Agirre. 2018. **[Unsupervised Statistical Machine Translation](https://arxiv.org/pdf/1809.01272.pdf)**. In *Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP 2018)*.

If you use this software for academic research, please cite the paper in question:
```
@inproceedings{artetxe2018emnlp,
  author    = {Artetxe, Mikel  and  Labaka, Gorka  and  Agirre, Eneko},
  title     = {Unsupervised Statistical Machine Translation},
  booktitle = {Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing},
  month     = {November},
  year      = {2018},
  address   = {Brussels, Belgium},
  publisher = {Association for Computational Linguistics}
}
```

Usage is equivalent to word2vec, with the addition of an optional parameter `--phrases <file>` to specify the set of phrases (one per line) to learn embeddings for. For best results, we recommend disabling subsampling (i.e. `--sample 0`). Here is an example call with the hyperparameters used in our experiments:
```
./word2vec -cbow 0 -hs 0 -sample 0 -size 300 -window 5 -negative 10 -iter 5 \
           -train CORPUS.TXT \
           -phrases PHRASES.TXT \
           -output OUTPUT.TXT
```

For more details on word2vec, please refer to the original README at `README-original.txt`.
