# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Get Wiki Corpus and Transform into ZhTW

import logging
import os
from tqdm import tqdm
import argparse
import opencc
from gensim.corpora import WikiCorpus

logger = logging.getLogger(__name__)
converter = opencc.OpenCC("s2twp.json")


def parse_args():

    parser = argparse.ArgumentParser(description="Extract Wiki Corpus To File.")
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

    """ Create Output Directory """
    if not os.path.exists(os.path.dirname(args.OUTPUT)):
        os.makedirs(os.path.dirname(args.OUTPUT))

    """ Extract AND Transform zhtw """
    wiki_corpus = WikiCorpus(fname=args.INPUT, dictionary={})
    count = 0
    with open(args.OUTPUT, "w", encoding="utf-8") as output:
        for text in tqdm(wiki_corpus.get_texts()):

            orig_text = " ".join(text) + "\n"
            zhtw_text = converter.convert(orig_text)
            output.write(zhtw_text)
            count += 1


if __name__ == "__main__":
    main()