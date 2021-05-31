# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Get Wiki Corpus and Transform into ZhTW

import logging
import os
from tqdm import tqdm
import argparse
import opencc
from gensim.corpora import WikiCorpus
from ckip_transformers.nlp import CkipWordSegmenter

logger = logging.getLogger(__name__)
converter = opencc.OpenCC("s2twp.json")
ws_driver = CkipWordSegmenter(level=3)


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

    """ Preprocess """
    ## Extract wiki corpus
    wiki_corpus = WikiCorpus(fname=args.INPUT, dictionary={})
    count = 0
    tmp_articles = list()
    with open(args.OUTPUT, "w", encoding="utf-8") as output:
        for text in tqdm(wiki_corpus.get_texts()):

            orig_text = " ".join(text)

            ## Transform zh-cn into zh-tw
            zhtw_text = converter.convert(orig_text)
            tmp_articles.append(zhtw_text)
            count += 1

            ## Every 10000 articles, tokenize them once.
            if count % 10000 == 0:
                tokenized_articles = ws_driver(tmp_articles)
                for tokenized_zhtw_text in tokenized_articles:
                    tmp_text = " ".join(tokenized_zhtw_text) + "\n"
                    output.write(tmp_text)
                tmp_articles = list()

        if tmp_articles:
            tokenized_articles = ws_driver(tmp_articles)
            for tokenized_zhtw_text in tokenized_articles:
                tmp_text = " ".join(tokenized_zhtw_text) + "\n"
                output.write(tmp_text)
            tmp_articles = list()


if __name__ == "__main__":
    main()