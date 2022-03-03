# singlish-english-nmt
 
 Despite the success of sequence-to-sequence RNN and Transformer models in Machine Translation (MT) tasks, most tasks still require a large parallel corpus. However, the progress in Unsupervised MT research has allowed for building of MT models without the need for parallel data, solely relying on monolingual corpora. This repository serves to explore the implementation of Undreamt, an unsupervised neural translation model, on Singlish-English translation tasks. The complete model is able to successfully learn Singlish-English word translations, but was unable to go beyond word-to-word translations. To the best of my knowledge, this is the first significant work done on Singlish-English machine translation.
 
 This readme file provides a step-by-step explanation on how to reproduce the results. First, clone the repository.

```
git clone https://github.com/justinpeh97/singlish-english-nmt.git
cd singlish-english-nmt
```

Installing dependencies
```
conda create -n senmt
conda activate senmt
pip install -r requirements.txt
```

 # Generation of datasets
 
 ### Reddit dataset
 
```
python3 reddit_scrape.py --client_id id --client_secret secret --user_agent agent
```
id, secret and agent are the client_id, client_secret and user_agent used to create the Reddit instance. They can be obtained by following the instructions on this website: https://towardsdatascience.com/scraping-reddit-data-1c0af3040768 . If you wish to change remove/add subreddits to the list of subreddits being scraped, simply edit the subreddit.txt file found in [data](https://github.com/justinpeh97/singlish-english-nmt/tree/main/data/generate_data) . The default number of posts scrapped per subreddit is 3000, which is found to generate around 13+ million sentences. If you wish to specify another number, use the optional argument --post_per_subreddit .

### Singlish dataset

```
python3 hwz_scraping.py 
```
If no arguments are specified, then all comments from all threads will be scraped. Scraping all 200000+ threads generated 13+ million sentences, hence on average there are 60+ sentences per thread. However, the number of sentences per thread varies greatly, with some thread having as few as <10 sentences, while others having over 100000 sentences. --max-per-thread controls the maximum number of comments to scrape from each thread and hence, controls the variability of the data. --num_threads controls the number of threads to scrape. --thread controls the URl of the thread to scrape from. The default is the EDMW thread.

## Dataset Preprocessing

There are 5 main dataset preprocessing operations:
1. Convert text to lowercase
2. Tokenization
3. Cleaning of text 
- Cleaning of English words (e.g. "actly" -> "actually", "alr" -> "already")
- Standardization / Cleaning of Singlish words (e.g "hao lian" -> "haolian")
4. Convert English to Singlish (e.g. "also" -> "oso"). Makes the Singlish dataset more "Singlish"
5. Filtering: Discard away sentences with no Singlish vocabulary

Steps 1 & 2 are common data preprocessing steps for machine translation. Steps 3-5 are novel cleaning steps for the Singlish dataset and is believed to improve model performance. To perform dataset preprocessing, simply run the following command:

```
bash process_datasets.sh
```

The bash script processes 4 datasets: Singlish test dataset, Singlish validation dataset, Singlish (HWZ) train dataset and English (Reddit) train dataset. Conversion to lower case and tokenization is applied to all 4 datasets. In addition, cleaning of text, conversion of English words to Singlish vocabulary is applied to all Singlish datasets. Lastly, filtering is done for the Singlish train dataset. The Singlish test/val datasets are manually chosen hence there is no need for filtering.

Steps 3, 4 and 5 consists of cleaning steps defined by 6 text files found in [data/data_processing](https://github.com/justinpeh97/singlish-english-nmt/tree/main/data/data_processing). singlish_vocab.txt is simply a text file containing all the singlish vocabulary used for filtering out non-Singlish sentences in the Singlish dataset. The other 5 datasets are cleaning steps that map a word to another word. For instance, the first line in the file clean_english_replace.txt, "alr,already", converts all instances of "alr" in the text to "already". To edit the list of handpicked rules, simply edit the file while maintening it in the same format.

![hey now](https://github.com/justinpeh97/singlish-english-nmt/blob/main/images/convert.PNG?raw=true)

# Training Phrase Embeddings

Artetxe et al.'s implementation of Phrase2vec, an extension of the popular word2vec, will be used for training of phrase embeddings. The phrase2vec folder is a forked repository of [monoses](https://github.com/artetxem/monoses), a repository used for training of the popular monoses unsupervised machine translation algorithm. The monoses repository is used as it provides the code to run the [Phrase2vec](https://github.com/artetxem/phrase2vec) algorithm. All credit goes to Artetxe and his team. To train the phrase embeddings, simply run the following commands:

```
cd phrase2vec
bash get-third-party.sh
cd third-party/phrase2vec
make
cd ./../../
python3 train.py 

```
[comment]: <> (python3 train.py --src_file ./../data/datasets/processed/cleaned_cleaned_corpus.src --trg_file ./../data/datasets/processed/cleaned_cleaned_corpus.trg)

# Training Cross Lingual Embeddings

Vecmap will be used for the training of cross-lingual embeddings. It is highly recommended to utilize GPU for vecmap training as it can help to achieve up to 50x increased training speed. The vecmap folder is a forked repository of the original [repository](https://github.com/artetxem/vecmap) created by Artetxe et al. To train the cross lingual embeddings, simply run the following commands:

```
cd vecmap
python3 map_embeddings.py --identical ./../embeddings/emb.src ./../embeddings/emb.trg   ./../embeddings/mapped_emb.src ./../embeddings/mapped_emb.trg   --cuda --verbose
```

It is necessary to first install the dependencies as instructed in the [here](https://github.com/artetxem/vecmap). Experiments were successfully ran with Cupy 10.1.0. Experimentation revealed that training using the --identical flag works best due to the large number of identical words between the English and Singlish vocabulary. It is also possible to train using the --unsupervised flag. The --semi_supervised flag can be used by providing a small seed dictionary of Singlish-English word pairs. To make use 

# Training the Unsupervised Neural Machine Translation model

The Undreamt model will be used for the training of the Unsupervised Neural Machine Translation model. Similar to vecmap, it is highly recommend to use GPU for training due to the large increase in training speed. The undreamt folder is a forked repository of the original [repository](https://github.com/artetxem/undreamt) created by Artetxe. To train the Undreamt model, simply run the following commands:

```
cd undreamt

python3 train.py    \
 --src ./../data/datasets/processed/cleaned_corpus.src    \
 --trg ./../data/datasets/processed/cleaned_corpus.trg    \
 --src_embeddings ./../embeddings/mapped_emb.src \ 
 --trg_embeddings ./../embeddings/mapped_emb.trg \
 --cutoff 400000 \
 --save model    \
 --save_interval 10000 \
 --cuda          \
 --iterations 150000   \
 --batch 25 \
 --hidden 800
```
It is necessary to first install PyTorch. Experiments were successfully ran with PyTorch 1.9.0. The above training command uses the best hyperparameters determined through hyperparameter tuning. To perform your own hyperparameter tuning, simply change/edit the --argument flags according to the instructions in the train.py file found [here](https://github.com/artetxem/undreamt/blob/master/undreamt/train.py). 


# Training platform

It is highly recommend to train the Vecmap and the Undreamt model using a GPU. Experimentations were done on NUS's High Performance Computing (HPC) clusters which uses Tesla V100-32GB GPUs. The Vecmap algorithm takes less than 10 minutes to train while the above command for Undreamt takes approximately 50 hours of training although it largely depends on the training set up (especially --iterations). Kaggle [servers](https://www.kaggle.com/code) as well as Google Colab [servers](https://colab.research.google.com/) provide free GPU for training models. Take note that the training set up might have to be adjusted to accomodate for the relatively smaller memory size of free GPU servers.

# Obtaining model results

## Undreamt 

To run the translation output of the Undreamt model on the test dataset, run the following command:

```
cd undreamt
python3 translate.py model.final.src2trg.pth -i ./../data/datasets/processed/test.sin.txt -o ./../data/datasets/model_output/undreamt_output.txt
```

## Word to Word model

A simple baseline model can be obtained by replacing each word in the source sentence with the closest word in the target sentence based on cosine similarity. To obtain the output of the word to word model, run the following command: 

```
python3 w2wmodel.py --sing embeddings/src_mapped.emb --eng embeddings/trg_mapped.emb --num_words 50000 --output_file data/datasets/model_output/w2w_output.txt --test_file data/datasets/processed/all.translations.txt

```

## Computing BLEU score

To obtain the BLEU score, first run nltk.download('all') and then run the following command:
```
python3 compute_bleu.py --candidate candidate_file --ref reference_file
```
candidate_file and reference_file refers to the location of the candidate file (model output) and reference file (human translation) respectively.
