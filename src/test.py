# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Inference

import logging
import json
from typing import List, Tuple
from gensim.models import word2vec
from gensim.models import KeyedVectors

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def load_model(use_fast: bool):
    if use_fast:
        wv = KeyedVectors.load(
            "model/word2vec_20210603040434_v250_c5_e5_s1.wordvectors", mmap="r"
        )
    else:
        model = word2vec.Word2Vec.load(
            "model/word2vec_20210603040434_v250_c5_e5_s1.model"
        )
        wv = model.wv
    return wv


def infer(wv, word: str, topn: int = 10) -> List[Tuple[str, float]]:
    if word not in wv:
        logger.info("{word} not in dictionary.")
        return None
    else:
        return wv.most_similar(word, topn=topn)


if __name__ == "__main__":

    logger.info("Load model ...")
    wv = load_model(use_fast=True)

    logger.info("Infer ...")
    ret = dict()
    with open(
        "/Users/allenyummy/Documents/news_classifier/src/utils/keywords/negative_news/NN_keywords.txt",
        "r",
        encoding="utf-8-sig",
    ) as f:

        for word in f:
            word = word.strip()

            ret[word] = list()
            if word in wv:
                res = infer(wv, word, topn=10)
                ret[word] = res

    logger.info("Writing file ...")
    with open("nn.json", "w", encoding="utf-8") as fo:
        json.dump(ret, fo, ensure_ascii=False, indent=4)
