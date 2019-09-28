from nltk.corpus import words
from nltk.tokenize.sonority_sequencing import SyllableTokenizer
import pandas as pd
import matplotlib.pyplot as plt
from stuff import SYLLABLE_REPLACEMENT

ssp = SyllableTokenizer()


def compress_word(word):
    syllables = ssp.tokenize(word)
    replaced = syllables.copy()
    for index, syl in enumerate(syllables):
        for symbol, replacement_syllables in SYLLABLE_REPLACEMENT.items():
            if syl in replacement_syllables:
                replaced[index] = symbol
    new_word = ''.join(replaced)
    return new_word


def compress_all():

    compressed = []

    for word in words.words():
        new_word = compress_word(word)
        if len(new_word) < len(word):
            compression = len(new_word)/len(word)
            compressed.append([
                word,
                new_word,
                len(word),
                compression,
            ])

    df = pd.DataFrame(
        compressed,
        columns=['old_word',
                 'new_word',
                 'old_word_length',
                 'compression',
                 ]
    )
    plt.scatter(df['compression'], df['old_word_length'])
    plt.show()


if __name__ == '__main__':
    compress_all()
