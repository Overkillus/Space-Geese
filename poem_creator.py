import countable
import scraper

import random
import inflect
import syllables
from urllib.error import URLError, HTTPError

inflect = inflect.engine()

verbs = ["have", "want", "like", "know", "saw", "hate", "love"]
third_verbs = ["has", "wants", "likes", "knows", "saw", "loves"]
third_people = ["Bob", "Ann", "Your mom", "Boris", "Donald", "Frankie"]
plural_people = ["Children", "Kids", "Brummies", "Farmers", "Coders", "Hackers", "We"]
beginnings = {"I": verbs, "They": verbs}
for p in third_people: 
    beginnings[p] = third_verbs
for p in plural_people: 
    beginnings[p] = verbs

def start_with_vowel(noun):
    vowels = ['a', 'e', 'i', 'o']
    return noun[0] in vowels

def get_start_sent_noun(noun):
    beginning = random.choice(list(beginnings.items()))
    subject = beginning[0]
    verb = random.choice(beginning[1])
    sent = subject + " " + verb + " "
    if countable.countable_noun(noun) and inflect.singular_noun(noun):
        if start_with_vowel(noun):
            sent += "an "
        else:
            sent += "a "
    sent += noun
    print(sent)
    if(estimate_syllables(sent) < 5):
        return get_start_sent_noun(noun)
    return sent

def estimate_syllables(sents):
    n_syl = 0
    for w in sents.split():
        n_syl += syllables.estimate(w)
    return n_syl

def get_start_sent_adj(adj):

    subject = random.choice(plural_people)
    str = subject + " are " + adj
    print(str)
    if estimate_syllables(str) < 5:
        return get_start_sent_adj(adj)
    return str



# f_out = open("sents_cows.txt", "w")


# for i in range(len(sents)):
#     f_out.write(" ".join(sents[i]) + '\n')
# for i in range(len(sents)):
#     if adjs[i]:
#         f_out.write(adjs[i] + '\n')
#     else: 
#         f_out.write("None"+ '\n')
# for i in range(len(sents)):
#     if nouns[i]:
#         f_out.write(nouns[i] + '\n')
#     else: 
#         f_out.write("None"+ '\n')

def get_random_noun_poem(sents, adjs, nouns):
    for i in range(len(nouns)):
        if nouns[i] != None:
            try:
                line1 = get_start_sent_noun(nouns[i])
                line2 = sents[i]
                return [line1, line2]
            except HTTPError as e:
                print("Error: " + str(e.code))

def get_random_adj_poem(sents, adjs, nouns):
    lines = None
    while lines == None:
        for i in range(len(adjs)):
            if adjs[i] != None:
                try:
                    line1 = get_start_sent_adj(adjs[i])
                    line2 = sents[i]
                    print(sents[i])
                    return [line1, line2]
                except HTTPError as e:
                    print("Error: " + str(e.code))

def get_random_full_poem():
    lines = None
    while lines == None:
        sents, adjs, nouns = scraper.get_random_stem_set()
        i = random.randint(0,1)
        if i == 0:
            lines = get_random_adj_poem(sents, adjs, nouns)
        elif i == 1:
            lines = get_random_noun_poem(sents, adjs, nouns)
        print(sents, adjs, nouns)
    lines = ["Roses are red"] + lines
    return lines
            
    
#######

print(get_random_full_poem())