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


def parse_args():

    parser = argparse.ArgumentParser(description="Extract Wiki Corpus To File.")
    parser.add_argument(
        "--input",
        type=str,
        help="input file path for wiki corpus",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="output txt file path",
    )
    parser.add_argument(
        "--gpu_index",
        type=int,
        default=-1,
        help="Setting this to -1 will leverage CPU, a positive will run the model on the associated CUDA device id.",
    )
    parser.add_argument(
        "--save_steps",
        type=int,
        default=5000,
        help="save to file every n steps",
    )
    parser.add_argument(
        "--debug",
        type=bool,
        default=False,
        help="debug mode",
    )
    args = parser.parse_args()
    return args


def main():

    """Args"""
    logger.info(" === PARSE ARGS === ")
    args = parse_args()
    logger.info(args)

    """ Language Converter """
    converter = opencc.OpenCC("s2twp.json")

    """ Tokenizer """
    tokenizer = CkipWordSegmenter(level=3, device=args.gpu_index)

    """ Create Output Directory """
    if not os.path.exists(os.path.dirname(args.output)):
        os.makedirs(os.path.dirname(args.output))

    """ Preprocess """
    logger.info(" === Preprocess === ")
    ## Extract wiki corpus
    wiki_corpus = WikiCorpus(fname=args.input, dictionary={})
    count = 0
    tmp_articles = list()
    with open(args.output, "w", encoding="utf-8") as output:
        for text in tqdm(wiki_corpus.get_texts()):

            ## SAVE 5 articles for debug mode
            if args.debug and count >= 5:
                break

            orig_text = " ".join(text)

            ## Transform zh-cn into zh-tw
            zhtw_text = converter.convert(orig_text)
            tmp_articles.append(zhtw_text)
            count += 1

            ## Every args.SAVE_STEPS articles, tokenize them once and save them.
            if count % args.save_steps == 0:
                tokenized_articles = tokenizer(tmp_articles)
                for tokenized_zhtw_text in tokenized_articles:
                    tmp_text = " ".join(tokenized_zhtw_text) + "\n"
                    output.write(tmp_text)
                tmp_articles = list()

        if tmp_articles:
            tokenized_articles = tokenizer(tmp_articles)
            for tokenized_zhtw_text in tokenized_articles:
                tmp_text = " ".join(tokenized_zhtw_text) + "\n"
                output.write(tmp_text)
            tmp_articles = list()


if __name__ == "__main__":
    main()
