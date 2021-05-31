# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Train own Word2Vec model

import logging
import argparse
from gensim.models import word2vec

logger = logging.getLogger(__name__)


def parse_args():

    parser = argparse.ArgumentParser(description="Train Word2Vec Model")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="input file path for wiki corpus",
        dest="INPUT",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="output txt file path",
        dest="OUTPUT",
    )
    args = parser.parse_args()
    return args


def main():

    """ Args """
    args = parse_args()

    """ Load Corpus """
    sentences = word2vec.LineSentence(args.INPUT)

    """ Train """
    model = word2vec.Word2Vec(sentences, vector_size=250, min_count=10)

    """ Save """
    model.save("word2vec.model")


if __name__ == "__main__":
    main()