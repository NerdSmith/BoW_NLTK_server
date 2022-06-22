import nltk
import numpy as np
nltk.download('punkt')
import re
import heapq


def collect_dataset(text):
    dataset = nltk.sent_tokenize(text)
    for i in range(len(dataset)):
        dataset[i] = dataset[i].lower()
        dataset[i] = re.sub(r'\W', ' ', dataset[i])
        dataset[i] = re.sub(r'\s+', ' ', dataset[i])
    return dataset


def word_to_count(ds):
    word2count = {}
    for data in ds:
        words = nltk.word_tokenize(data)
        for word in words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1
    return word2count


def get_most_frequently(dct, nb):
    return heapq.nlargest(nb, dct, key=dct.get)


def get_sentence_vectors(dataset, freq_words):
    sentence_vectors = []
    for data in dataset:
        vector = []
        for word in freq_words:
            if word in nltk.word_tokenize(data):
                vector.append(1)
            else:
                vector.append(0)
        sentence_vectors.append(vector)
    sentence_vectors = np.asarray(sentence_vectors)
    return sentence_vectors


if __name__ == '__main__':
    with open("test.txt", encoding="utf-8") as f:
        text = f.read()
    dataset = collect_dataset(text)
    w2c = word_to_count(dataset)
    freq_words = get_most_frequently(w2c, 20)
    print(freq_words)
    s_vectors = get_sentence_vectors(dataset, freq_words)
    print(s_vectors)
