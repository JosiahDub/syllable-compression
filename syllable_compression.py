from nltk.corpus import brown, words
from nltk.tokenize.sonority_sequencing import SyllableTokenizer
import pyphen
import pandas as pd
from matplotlib import colorbar
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
from stuff import SYLLABLE_REPLACEMENT

ssp = SyllableTokenizer()
dic = pyphen.Pyphen(lang='en')


def brown_words():
    return set(brown.words())


def words_words():
    return set(words.words())


def pyphen_syllables(word):
    return dic.inserted(word).split('-')


def nltk_syllables(word):
    return ssp.tokenize(word)


def compress_word(word, syllable_function):
    syllables = syllable_function(word)
    replaced = syllables.copy()
    for index, syl in enumerate(syllables):
        for symbol, replacement_syllables in SYLLABLE_REPLACEMENT.items():
            if syl in replacement_syllables:
                replaced[index] = symbol
    new_word = ''.join(replaced)
    return new_word


def compress_all(word_list, syllable_function):
    compressed = []
    for word in word_list:
        if '-' in word or '$' in word:
            continue
        new_word = compress_word(word, syllable_function)
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
        columns=[
            'old_word',
            'new_word',
            'old_word_length',
            'compression',
        ]
    )
    return df


def plot(df):
    all_points = list(zip(df['compression'], df['old_word_length']))
    unique_points = set(all_points)
    point_count = [all_points.count(point) for point in unique_points]
    cmap = get_cmap('gnuplot')
    normalize = Normalize(vmin=min(point_count), vmax=max(point_count))
    colors = [cmap(normalize(value)) for value in point_count]
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(
        [point[0] for point in unique_points],
        [point[1] for point in unique_points],
        color=colors,
        s=[100 for _ in range(len(unique_points))]
    )
    ax.set_xlabel('Compression Ratio', fontsize='xx-large')
    ax.set_ylabel('Original Word Length', fontsize='xx-large')
    cax, _ = colorbar.make_axes(ax)
    cbar = colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)
    cbar.ax.set_ylabel('Number of compressed words', fontsize='xx-large')
    # plt.show()
    plt.savefig('plot.png')


if __name__ == '__main__':
    compressed = compress_all(words_words(), pyphen_syllables)
    compressed.to_csv('raw_data.csv')
    plot(compressed)
