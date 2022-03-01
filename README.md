# singlish-english-nmt
 
 Despite the success of sequence-to-sequence RNN and Transformer models in Machine Translation (MT) tasks, most tasks still require a large parallel corpus. However, the progress in Unsupervised MT research has allowed for building of MT models without the need for parallel data, solely relying on monolingual corpora. This repository serves to explore the implementation of Undreamt, an unsupervised neural translation model, on Singlish-English translation tasks. The complete model is able to successfully learn Singlish-English word translations, but was unable to go beyond word-to-word translations. To the best of my knowledge, this is the first significant work done on Singlish-English machine translation.
 
 This readme file provides a step-by-step explanation on how to reproduce the results. 

```
git clone https://github.com/justinpeh97/singlish-english-nmt.git
```

 # Generation of datasets
 
 ### Reddit dataset
 
```
cd data/generate_data
python3 reddit_scrape.py --client_id id --client_secret secret --user_agent agent
```

id, secret and agent are the client_id, client_secret and user_agent used to create the Reddit instance. They can be obtained by following the instructions on this website: https://towardsdatascience.com/scraping-reddit-data-1c0af3040768 . If you wish to change remove/add subreddits to the list of subreddits being scraped, simply edit the subreddit.txt file found in [data](https://github.com/justinpeh97/singlish-english-nmt/tree/main/data/generate_train_data) . The default number of posts scrapped per subreddit is 3000, which is found to generate around 13+ million sentences. If you wish to specify another number, use the optional argument --post_per_subreddit .

### Singlish dataset

```
python3 hwz_scrape.py 
```
If no arguments are specified, then all comments from all threads will be scraped. Scraping all 200000+ threads generated 13+ million sentences, meaning that on average, there are 60+ sentences per thread. However, the number of sentences per thread varies greatly, with some thread having as few as <10 sentences, while others having over 100000 sentences. --max_per_thread controls the maximum number of comments to scrape from each thread and hence, controls the variability of the data. --num_threads controls the number of threads to scrape. --thread controls the URl of the thread to scrape from. The default is the EDMW thread.

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
cd data
bash process_datasets.sh
```

The bash script processes 4 datasets: Singlish test dataset, Singlish validation dataset, Singlish (HWZ) train dataset and English (Reddit) train dataset. Conversion to lower case and tokenization is applied to all 4 datasets. In addition, cleaning of text, conversion of English words to Singlish vocabulary is applied to all Singlish datasets. Lastly, filtering is done for the Singlish train dataset. The Singlish test/val datasets have already been manually filtered.

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


# Obtaining model results

## Word to Word model

A simple baseline model can be obtained by replacing each word in the source sentence with the closest word in the target sentence based on cosine similarity. To obtain the output of the word to word model, simply run the following command: 

```
python w2wmodel.py --sing embeddings/src_mapped.emb --eng embeddings/trg_mapped.emb --num_words 50000 --output_file data/datasets/model_output/w2w_output.txt --test_file data/datasets/processed/all.translations.txt
```

## Other experiments

## Things to update 
- BLEU/METEOR score
