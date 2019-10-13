import pandas as pd
from syllable_compression import plot

pyphen_words = pd.read_csv('pyphen_words.csv')
plot(pyphen_words, 'pyphen_words.png')

pyphen_brown = pd.read_csv('pyphen_brown.csv')
plot(pyphen_brown, 'pyphen_brown.png')

nltk_brown = pd.read_csv('nltk_brown.csv')
plot(nltk_brown, 'nltk_brown.png')

nltk_words = pd.read_csv('nltk_words.csv')
plot(nltk_words, 'nltk_words.png')
