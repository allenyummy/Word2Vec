#!/bin/bash

## Find Zh-Wiki Here: https://dumps.wikimedia.org/zhwiki/
curl -O https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2 && \
mkdir data && \
mv zhwiki-latest-pages-articles.xml.bz2 data

## Get Wiki Corpus And Transform ZhTW
echo ===== Proprocess Corpus =====

WIKI_INPUT_PATH=data/zhwiki-latest-pages-articles.xml.bz2
WIKI_OUTPUT_PATH=data/processed/wiki_corpus.txt
GPU_INDEX=-1  ## -1 means cpu
SAVE_STEPS=5000
DEBUG=False

python src/wiki2txt.py \
    --input $WIKI_INPUT_PATH \
    --output $WIKI_OUTPUT_PATH \
    --gpu_index $GPU_INDEX \
    --save_steps $SAVE_STEPS \
    --debug $DEBUG \


## Train Word2Vec model
echo ===== Train Word2Vec Model =====

TODAY=$(date +"%Y%m%d%H%M%S")
VECTOR_SIZE=250
MIN_COUNT=5
EPOCHS=5
SEED=1
TRAINED_MODEL_PATH=model/word2vec_${TODAY}_v${VECTOR_SIZE}_c${MIN_COUNT}_e${EPOCHS}_s${SEED}.model

python src/train.py \
    --input $WIKI_OUTPUT_PATH \
    --output $TRAINED_MODEL_PATH \
    --vector_size $VECTOR_SIZE \
    --min_count $MIN_COUNT \
    --epochs $EPOCHS \
    --seed $SEED \