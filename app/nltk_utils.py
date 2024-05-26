import numpy as np
from nltk.stem.porter import PorterStemmer
from underthesea import word_tokenize

stemmer = PorterStemmer()


def tokenize(sentence):
    """
    split sentence into array of words/tokens
    a token can be a word or punctuation character, or number
    Tách câu thành mảng các từ/tokens.
    Ví dụ: "Hello, how are you?" sẽ được tách thành ["Hello", ",", "how", "are", "you", "?"].

    """
    return word_tokenize(sentence)


def stem(word):
    """
    Chuyển đổi từ về dạng gốc (stem).
    stemming = find the root form of the word
    examples:
    words = ["organize", "organizes", "organizing"]
    words = [stem(w) for w in words]
    -> ["organ", "organ", "organ"]
    """
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    """
    Tạo ra một vector Bag of Words cho một câu đã token hóa.
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1

    return bag
