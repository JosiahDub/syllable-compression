from syllable_compression import pyphen_syllables, nltk_syllables, compress_all, brown_words, words_words

pyphen_words = compress_all(words_words(), pyphen_syllables)
pyphen_words.to_csv('pyphen_words.csv')

pyphen_brown = compress_all(brown_words(), pyphen_syllables)
pyphen_brown.to_csv('pyphen_brown.csv')

nltk_words = compress_all(words_words(), nltk_syllables)
nltk_words.to_csv('nltk_words.csv')

nltk_brown = compress_all(brown_words(), nltk_syllables)
nltk_brown.to_csv('nltk_brown.csv')
