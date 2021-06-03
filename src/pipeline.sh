#!/bin/bash

#######################################################

## Check if current working directory is "/home/username/Word2Vec"
case $(pwd) in
*/Word2Vec) echo "Working dir ($(pwd)) is correct." ;;
*)
    echo "Make sure working dir is '/home/usrname/Word2Vec'."
    exit
    ;;
esac

## Check if "data/" exists
DIR=data/
if [ ! -d "$DIR" ]; then
    echo "$DIR does not exist, so create it."
    mkdir $DIR
fi

## Check if "data/zhwiki-latest-pages-articles.xml.bz2" exists
FILE=data/zhwiki-latest-pages-articles.xml.bz2
if [ ! -f "$FILE" ]; then
    echo "$FILE does not exist, so curl and move it."
    ## Find Zh-Wiki Here: https://dumps.wikimedia.org/zhwiki/
    curl -O https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2
    mv zhwiki-latest-pages-articles.xml.bz2 data
fi

#######################################################

function description {
    echo "description: bash src/pipeline.sh --preprocess --train"
    echo "   "
    echo "  -p | --preprocess     :  whether to preprocess corpus"
    echo "  -d | --debug          :  whether to open debug mode for preprocessing stage"
    echo "  -t | --train          :  whether to train Word2Vec model"
    echo "  -h | --help           :  help description"
}

function parse_args {

    preprocess=false
    debug=false
    train=false

    while [ "$1" != "" ]; do
        case "$1" in
        -p | --preprocess) preprocess=true ;;
        -d | --debug) debug=true ;;
        -t | --train) train=true ;;
        -h | --help)
            description
            exit
            ;;
        *) echo "$1 is not supported." ;;
        esac
        shift
    done
}

#######################################################

## parse args
parse_args $@
echo preprocess=$preprocess, debug=$debug, train=$train

#######################################################

## Preprocess corpus
WIKI_INPUT_PATH=data/zhwiki-latest-pages-articles.xml.bz2
WIKI_OUTPUT_PATH=data/processed/wiki_corpus.txt
SAVE_STEPS=5000

if $preprocess && ! $debug; then

    echo ===== Preprocess Corpus =====
    python src/wiki2txt.py \
        --input $WIKI_INPUT_PATH \
        --output $WIKI_OUTPUT_PATH \
        --save_steps $SAVE_STEPS

elif $preprocess && $debug; then

    echo ===== Preprocess Corpus with Debug Mode =====
    WIKI_OUTPUT_PATH=data/processed/wiki_corpus_debug.txt
    python src/wiki2txt.py \
        --input $WIKI_INPUT_PATH \
        --output $WIKI_OUTPUT_PATH \
        --save_steps $SAVE_STEPS \
        --debug

else

    echo ===== No Preprocess =====
    if [ ! -f "$WIKI_OUTPUT_PATH" ]; then
        echo "$WIKI_OUTPUT_PATH does not exist, so please add --preprocess."
    fi

fi

#######################################################

## Train Word2Vec model
TODAY=$(date +"%Y%m%d%H%M%S")
VECTOR_SIZE=250
MIN_COUNT=5
EPOCHS=5
SEED=1
TRAINED_MODEL_PATH=model/word2vec_${TODAY}_v${VECTOR_SIZE}_c${MIN_COUNT}_e${EPOCHS}_s${SEED}.model

if $train; then

    echo ===== Train Word2Vec Model =====
    python src/train.py \
        --input $WIKI_OUTPUT_PATH \
        --output $TRAINED_MODEL_PATH \
        --vector_size $VECTOR_SIZE \
        --min_count $MIN_COUNT \
        --epochs $EPOCHS \
        --seed $SEED

else
    echo ===== No training =====
fi
