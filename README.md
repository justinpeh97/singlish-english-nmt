# singlish-english-nmt
 
 Despite the success of sequence-to-sequence RNN and Transformer models in Machine Translation (MT) tasks, most tasks still require a large parallel corpus. However, the progress in Unsupervised MT research has allowed for building of MT models without the need for parallel data, solely relying on monolingual corpora. This repository serves to explore the implementation of Undreamt, an unsupervised neural translation model, on Singlish-English translation tasks. The complete model is able to successfully learn Singlish-English word translations, but was unable to go beyond word-to-word translations. To the best of my knowledge, this is the first significant work done on Singlish-English machine translation.
 
 This readme file provides a step-by-step explanation on how to reproduce the results found in __. 

```
git clone https://github.com/justinpeh97/singlish-english-nmt.git
```

 ## Generation of datasets
 
 ### Reddit dataset
 
```
cd data
python reddit_scrape.py --client_id id --client_secret secret --user_agent agent
```

Where id, secret and agent are the client_id, client_secret and user_agent used to create the Reddit instance. They can be obtained by following the instructions on this website: https://towardsdatascience.com/scraping-reddit-data-1c0af3040768 . If you wish to change remove/add subreddits to the list of subreddits being scraped, simply edit the subreddit.txt file found in [data](https://github.com/justinpeh97/singlish-english-nmt/tree/main/data) . The default number of posts scrapped per subreddit is 3000, which is found to generate around 13+ million sentences. If you wish to specify another number, use the optinal argument --post_per_subreddit .

### Singlish dataset

```
python hwz_scrape.py 
```

Optional arguments: 

| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| -sc --scorecutoff 	       |	0.1           |the score from the classifier for each C position
| -p  --pruncutoff          | 0.1           |the SVM score checked for consecutive Cs from both ends to refine the boundaries
| -npp -–numprocess 	       |	8	            |number of cores to be used
| -ml --minlength  		       | 50	           | minimum length of DMRs required to be reported 
| -ncb --numcb 		           | 5             | minimum number of Cs present between DMRs to keep them seperate
| -md  -–mergedist 	        | 500           | maximum distance allowed between DMRs to merge 
| -prn --prunningC	         | 3             | number of consecutives Cs to be considered for pruning for boundary refinement2
| -ns --numsamples          | all           | no.of samples to use for DMR calling; default takes all sample in the file
| -sp --startposition       | 1st position  | start position of sample in the sample file to use for timeseries DMR calling 
| -BSSeeker2 --BSSeeker2    | False         | input CGmap file from BSSeeker2
| -mc --minc			             | 3 	           | minimum number of Cs in a DMR
| -sin --singlechrom			     | False         | parallel code for single chromosome; *npp* will be used for parallel run for each chr
| -d --delta			             | 0.1     	     | minimum average difference in methylation required in a DMR 
| -wrt --withrespectto		    | all     	     | samples to use for DMR calling for pairwise comparisions with respect to specific samples
| -Keepall --Keepall		      | False     	   | Keep all cytosine positions present in atleast one of the replicate

### News Crawl dataset


## To do

Add in English cleaning algorithm \\
Mention News Crawl

## Other experiments
