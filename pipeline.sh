#!/bin/bash

## Find Zh-Wiki Here: https://dumps.wikimedia.org/zhwiki/
## curl -O https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2 

## Get Wiki Corpus And Transform ZhTW
WIKI_INPUT_PATH="/Users/allenyummy/Documents/Word2Vec/data/zhwiki-latest-pages-articles.xml.bz2"
WIKI_OUTPUT_PATH="/Users/allenyummy/Documents/Word2Vec/data/processed/wiki_corpus.txt"

python wiki2txt.py \
    -i $WIKI_INPUT_PATH \
    -o $WIKI_OUTPUT_PATH \