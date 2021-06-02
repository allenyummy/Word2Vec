# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Train own Word2Vec model

import logging
import os
import argparse
from gensim.models import word2vec

logger = logging.getLogger(__name__)


def parse_args():

    parser = argparse.ArgumentParser(description="Train Word2Vec Model")
    parser.add_argument(
        "--input",
        type=str,
        help="input file path for wiki corpus",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="output model path",
    )
    parser.add_argument(
        "--vector_size",
        type=int,
        default=250,
        help="Dimensionality of the word vectors.",
    )
    parser.add_argument(
        "--min_count",
        type=int,
        default=5,
        help="Ignores all words with total frequency lower than this.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=5,
        help="Number of iterations (epochs) over the corpus.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=1,
        help="Initial vectors for each word are seeded with a hash of the concatenation of word + str(seed).",
    )

    args = parser.parse_args()
    return args


def main():

    """ Args """
    args = parse_args()

    """ Create Output Directory """
    if not os.path.exists(os.path.dirname(args.output)):
        os.makedirs(os.path.dirname(args.output))

    """ Load Corpus """
    sentences = word2vec.LineSentence(args.input)

    """ Train """
    model = word2vec.Word2Vec(
        sentences,
        vector_size=args.vector_size,
        min_count=args.min_count,
        seed=args.seed,
        epochs=args.epochs,
    )

    """ Save """
    model.save(args.output)


if __name__ == "__main__":
    main()