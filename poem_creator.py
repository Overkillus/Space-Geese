import countable
import scraper

import random
import inflect
from urllib.error import URLError, HTTPError

inflect = inflect.engine()

verbs = ["have", "want", "like", "know", "saw", "hate", "love"]
third_verbs = ["has", "wants", "likes", "knows", "saw", "loves"]
third_people = ["Bob", "Ann"]
plural_people = ["Children", "Kids", "Brummies", "Farmers", "Coders", "Hackers"]
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
    return sent

def get_start_sent_adj(adj):

    subject = random.choice(plural_people)
    str = subject + " are " + adj
    return str



f_out = open("sents_cows.txt", "w")

r2 = scraper.get_results_cows()
l2 = scraper.cow_results_to_words(r2)




sents, adjs, nouns = scraper.find_sents_and_adjs(l2)
for i in range(len(sents)):
    f_out.write(" ".join(sents[i]) + '\n')
for i in range(len(sents)):
    if adjs[i]:
        f_out.write(adjs[i] + '\n')
    else: 
        f_out.write("None"+ '\n')
for i in range(len(sents)):
    if nouns[i]:
        f_out.write(nouns[i] + '\n')
    else: 
        f_out.write("None"+ '\n')

for i in range(len(nouns)):
    if nouns[i] != None:
        try:
            get_start_sent_noun(nouns[i])
            print(sents[i])
        except HTTPError as e:
            print("Error: " + str(e.code))

for i in range(len(adjs)):
    if adjs[i] != None:
        try:
            get_start_sent_adj(adjs[i])
            print(sents[i])
        except HTTPError as e:
            print("Error: " + str(e.code))
        
    
#######
