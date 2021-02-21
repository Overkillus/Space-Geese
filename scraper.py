from re import search
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pronouncing
import random


import nltk
# nltk.download("brown")
# nltk.download("wordnet")
from nltk.corpus import brown
from nltk.corpus import wordnet as wn

def get_results():
    url = "https://www.bbc.com/news/topics/c256e4q7z8zt/geese"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all("span", {"class": "lx-stream-post__header-text"})
    return results

def get_results_cows():
    url = "https://www.bbc.com/news/topics/c2d2m3e1p96t/cattle"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all("span", {"class": "lx-stream-post__header-text"})
    # print(results)
    return results

def get_results_chickens():
    url = "https://www.bbc.com/news/topics/cqlyx9q32g8t/chickens"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all("span", {"class": "lx-stream-post__header-text"})
    # print(results)
    return results


def get_random_result(results):
    return [random.choice(results)]

sents = []
goose_words = ["goose", "geese", "Goose", "Geese", "gosling", "Gosling", "goslings", "Goslings", "goose's", "geese's", "Goose's", "Geese's"]

def contains_goose_word(words):
    for w in goose_words:
        if w in words:
            return True
    return False

def find_first_adj(words):
    for w in words:
        if wn.synsets(w):
            synsets = wn.synsets(w)
            for s in synsets:
                if s.pos() == "a" or s.pos() == "s":
                    return w
    return None

def find_first_noun(words):
    for w in words:
        if wn.synsets(w):
            synsets = wn.synsets(w)
            for s in synsets:
                if s.pos() == "n":
                    return w
    return None

def goosify(sent):
    l = sent.split()
    print(l)
    for i in range(len(l)):
        if l[i] == "cow's":
            l[i] = "goose's"
        elif l[i] == "Cow's":
            l[i] = "Goose's"
        elif l[i] == "cow":
            l[i] = "goose"
        elif l[i] == "Cow":
            l[i] = "Goose"
        elif l[i] == "Cows":
            l[i] = "Geese"
        elif l[i] == "cows":
            l[i] = "geese"
            # chicks
        elif l[i] == "chickens" or l[i] == "chicks":
            l[i] = "geese"
        elif l[i] == "Chickens" or l[i] == "Chicks":
            l[i] = "Geese"
        elif l[i] == "chicken":
            l[i] = "goose"
        elif l[i] == "hens":
            l[i] = "geese"
        elif l[i] == "Chicken":
            l[i] = "Goose"
    return l

def results_to_words(results):
    l = []
    for r in results:
        r_words = r.text.split(" ")
        l.append(r_words)
    return l

def cow_results_to_words(results):
    l = []
    for r in results:
        print(r.text)
        # txt = r.text.replace('''):
         
        r_words = goosify(r.text)
        l.append(r_words)
    return l


def find_sents_and_adjs(r_words_list):
    sents = []
    adjs = []
    nouns = []
    for r_words in r_words_list:
        if contains_goose_word(r_words):
            sents.append(" ".join(r_words))
            # print(r_words[-1])
            rhymes = pronouncing.rhymes(r_words[-1])
            freqs = nltk.FreqDist([w.lower() for w in brown.words()])
            # sort wordlist by word frequency
            wordlist_sorted = sorted(rhymes, key=lambda x: freqs[x.lower()], reverse=True)
            # print the sorted list
            # print(r_words[-1])
            # print(wordlist_sorted)
            adj = find_first_adj(wordlist_sorted)
            n = find_first_noun(wordlist_sorted)
            adjs.append(adj)
            nouns.append(n)
    # print(sents)
    # print(adjs)
    # print(nouns)
    return sents, adjs, nouns

# def goosify(sent):
#     l = sent.split()
#     for i in range(len(l)):
#         if l[i] == "cow's":
#             l[i] = "goose's"
#         elif l[i] == "Cow's":
#             l[i] = "Goose's"
#         elif l[i] == "cow":
#             l[i] = "goose"
#         elif l[i] == "Cow":
#             l[i] = "Goose"
#         elif l[i] == "Cows":
#             l[i] = "Geese"
#         elif l[i] == "cows":
#             l[i] = "geese"
#     return l



def get_random_stem_set():
    r1 = get_results()
    r1 = results_to_words(r1)
    r2 = get_results_cows()
    r2 = cow_results_to_words(r2)
    r3 = get_results_chickens()
    r3 = cow_results_to_words(r3)
    r = r1 + r2 + r3
    result = get_random_result(r3)
    sents, adjs, nouns = find_sents_and_adjs(result)
    print("PRINTING RESULTS IN SCAPER")
    print(sents, adjs, nouns)
    if not (sents == [] or (adjs == [None] and nouns == [None])):
        return sents, adjs, nouns
    else: 
        return get_random_stem_set()


