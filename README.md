# Word2Vec

該 repo 展示如何訓練自己的 Word2Vec 模型，雖然 Word2Vec 是 2013 年的產物，無法處理一詞多義的狀況，但是仍是一個值得學習的經典模型。

---

<a name="toc"/></a>
## Table of Contents
* Installation(#installation)
* Prepare Corpus(#prepare_corpus)
* Train your own Word2Vec model(#train)
* Example(#example)


<a name="installation"/></a>
## Installation

* Prepare conda virtual environment
```
$ conda create --name Word2Vec-py38 python=3.8
$ conda activate Word2Vec-py38
$ git clone https://github.com/allenyummy/Word2Vec.git
$ cd Word2Vec
$ pip install -r requirements.txt
```

* Prepare development environment by building docker image by your own.
```
$ git clone https://github.com/allenyummy/Word2Vec.git
$ cd Word2Vec
$ docker build -t word2vec-zhtw . --no-cache
```
Then, an image called "word2vec-zhtw" would be built up successfully.

* Prepare developement environment by downlaoding a docker image that was already built in docker hub.
```
$ docker pull allenyummy/word2vec-zhtw
```

* (Optional, If Needed) Prepare development environment by downloading a docker image that contains three ckip-transformers-word-segment-models.

This may be helpful when the operating server is not allowed to connent to Internet.

The reason why it may be helpful is that this repo uses ckip models to tokenize documents in the preprocessing stage. Before doing that, it could automatically downlaod the models from huggingface model hub with Internet. However, if you have no Internet, the image (allenyummy/word2vec-zhtw-ckip-ws-models:latest) have already contained three models. You can use this image without Internet.

You may ask how we pull the image if we are not allowed to connenct to Internet. No you don't. So you have to save the image into .tar file in certain environment that has Internet and then transmit it in some way into the server. Good Luck.
```
$ docker pull allenyummy/word2vec-zhtw-ckip-ws-models:latest
```
Note that this image includes three ckip-transformers-word-segement-models.
1. [ckiplab/bert-base-chinese-ws](https://huggingface.co/ckiplab/bert-base-chinese-ws)
2. [ckiplab/albert-base-chinese-ws](https://huggingface.co/ckiplab/albert-base-chinese-ws)
3. [ckiplab/albert-tiny-chinese-ws](https://huggingface.co/ckiplab/albert-tiny-chinese-ws)

* Launch a docker container by the image you download in the above step
```
$ docker run -it --rm --name container -v /home/allenyummy/Word2Vec:/workspace word2vec-zhtw:latest
```

---
<a name="prepare_corpus"/></a>
## Prepare Corpus

The final format of corpus should be a file.txt. Also, in the file.txt, each document one line and it must be tokenized. For example:
```
歐幾裡得   西元 前 三世紀 的 古希臘 數學家   現在 ... [First document/sentence]
我 是 神奇 寶貝 ...  [Second document/sentence]
```

Once prepared, then it could be loaded by gensim.models.word2vec.LineSentence.
```
from gensim.models import LineSentence
sentences = word2vec.LineSentence(file.txt)
```

---
<a name="train"/></a>
## Train your own Word2Vec model
```
model = word2vec.Word2Vec(
    sentences,
    vector_size=args.vector_size,
    min_count=args.min_count,
    seed=args.seed,
    epochs=args.epochs,
)

model.save("word2vec.model")
```

---
<a name="example"/></a>
## Example
In this repo, we use wiki as an example. We need to download it first [URL](https://dumps.wikimedia.org/zhwiki/) or `curl` it.
```
$ curl -O https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2 
```

Run pipeline.sh
```
$ bash src/pipeline.sh
```
```
#!/bin/bash

## Find Zh-Wiki Here: https://dumps.wikimedia.org/zhwiki/
## curl -O https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2 

## Get Wiki Corpus And Transform ZhTW
echo ===== Proprocess Corpus =====

WIKI_INPUT_PATH=data/zhwiki-latest-pages-articles.xml.bz2
WIKI_OUTPUT_PATH=data/processed/wiki_corpus_5.txt
GPU_INDEX=-1  ## -1 means cpu
SAVE_STEPS=5000
DEBUG=True

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
```

