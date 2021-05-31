from gensim.test.utils import datapath
from gensim import utils
from gensim.models import word2vec


class MyCorpus:
    """An iterator that yields sentences (lists of str)."""

    def __iter__(self):
        corpus_path = datapath("lee_background.cor")
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield utils.simple_preprocess(line)


if __name__ == "__main__":
    # sentences = MyCorpus()
    # for i, sentence in enumerate(sentences):
    #     if i > 1:
    #         break
    #     print(sentence)

    model = word2vec.Word2Vec.load("word2vec.model")
    for index, word in enumerate(model.wv.index_to_key):
        if index == 20:
            break
        print(f"word #{index}/{len(model.wv.index_to_key)} is {word}")

    vec_history = model.wv["歷史"]
    print(len(vec_history))
    print(model.wv.most_similar("文學", topn=5))
