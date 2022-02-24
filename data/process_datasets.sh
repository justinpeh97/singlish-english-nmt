#!/bin/bash

python dataset_processing.py --input_file ./datasets/raw/test.sin.raw.txt --output_file ./datasets/processed/test.sin.txt  --lower --tokenize --clean_text --english_to_singlish
python dataset_processing.py --input_file ./datasets/raw/val.sin.raw.txt --output_file ./datasets/processed/val.sin.txt  --lower --tokenize --clean_text --english_to_singlish
python dataset_processing.py --input_file ./datasets/raw/raw_singlish.txt --output_file ./datasets/processed/singlish.txt  --lower --tokenize --clean_text --english_to_singlish --filtering
python dataset_processing.py --input_file ./datasets/raw/raw_reddit.txt --output_file ./datasets/processed/reddit.txt  --lower --tokenize