# singlish-english-nmt
 
 Despite the success of sequence-to-sequence RNN and Transformer models in Machine Translation (MT) tasks, most tasks still require a large parallel corpus. However, the progress in Unsupervised MT research has allowed for building of MT models without the need for parallel data, solely relying on monolingual corpora. This repository serves to explore the implementation of Undreamt, an unsupervised neural translation model, on Singlish-English translation tasks. The complete model is able to successfully learn Singlish-English word translations, but was unable to go beyond word-to-word translations. To the best of my knowledge, this is the first significant work done on Singlish-English machine translation.
 
 This readme file provides a step-by-step explanation on how to reproduce the results found in __. 

```
git clone https://github.com/justinpeh97/singlish-english-nmt.git
```

 ## Generation of datasets
 
 ### Reddit dataset
 
```
cd data/generate_train_data
python reddit_scrape.py --client_id id --client_secret secret --user_agent agent
```

Where id, secret and agent are the client_id, client_secret and user_agent used to create the Reddit instance. They can be obtained by following the instructions on this website: https://towardsdatascience.com/scraping-reddit-data-1c0af3040768 . If you wish to change remove/add subreddits to the list of subreddits being scraped, simply edit the subreddit.txt file found in [data](https://github.com/justinpeh97/singlish-english-nmt/tree/main/data) . The default number of posts scrapped per subreddit is 3000, which is found to generate around 13+ million sentences. If you wish to specify another number, use the optinal argument --post_per_subreddit .

### Singlish dataset

```
python hwz_scrape.py 
```

Optional arguments: 

| Argument                  | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| --num_threads	            |	None   | Number of threads to scrape. If not specified (default = None), then all the threads will be scraped.
| --max_per_thread          | 500000000  | Maximum number of comments to scrape from each thread. Default number is an arbitrarily large number which means that all comments will be sraped. 
| --thread 	                |	"https://forums.hardwarezone.com.sg/forums/eat-drink-man-woman.16" 	| Thread to scrape from. Default is EDMW thread.
| --output 		               | "hwz_sentences.txt"	 | Name of output file. 



## Dataset Preprocessing

There are 5 main dataset preprocessing operations:
1. Convert text to lowercase - Eases model training
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

The bash script processes 4 datasets:  test dataset of Singlish sentences, validation dataset of Singlish sentences, raw English sentences (from Reddit), raw Singlish sentences (from HardwareZone). Conversion to lower case and tokenization is performed for the test/val Singlish datasets as well as the raw English dataset. Conversion to lower case, tokenization, cleaning of text, conversion of English words to Singlish vocabulary and filtering is done for the raw Singlish sentences.


## To do

Mention where to put datasets



## Other experiments
