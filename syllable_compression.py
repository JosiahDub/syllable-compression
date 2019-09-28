import csv
from nltk.corpus import brown
from nltk.tokenize.sonority_sequencing import SyllableTokenizer
import pyphen
import pandas as pd
import matplotlib.pyplot as plt
from stuff import SYLLABLE_REPLACEMENT

ssp = SyllableTokenizer()
dic = pyphen.Pyphen(lang='en')


def compress_word(word):
    # syllables = ssp.tokenize(word)
    syllables = dic.inserted(word).split('-')
    replaced = syllables.copy()
    for index, syl in enumerate(syllables):
        for symbol, replacement_syllables in SYLLABLE_REPLACEMENT.items():
            if syl in replacement_syllables:
                replaced[index] = symbol
    new_word = ''.join(replaced)
    return new_word


def compress_all():
    compressed = []
    for word in brown.words():
        if word.startswith('-') or word.endswith('-'):
            continue
        new_word = compress_word(word)
        if len(new_word) < len(word):
            compression = len(new_word)/len(word)
            compressed.append([
                word,
                new_word,
                len(word),
                compression,
            ])
    return compressed


def plot(data):
    df = pd.DataFrame(
        data,
        columns=[
            'old_word',
            'new_word',
            'old_word_length',
            'compression',
        ]
    )
    plt.scatter(df['compression'], df['old_word_length'])
    plt.show()


if __name__ == '__main__':
    compressed = compress_all()
    with open('raw_data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Old word', 'New word', 'Old word length', 'Compression'])
        for compress in compressed:
            writer.writerow(compress)
    plot(compressed)
