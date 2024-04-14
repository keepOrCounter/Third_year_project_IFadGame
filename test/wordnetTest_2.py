# import nltk
# from nltk.corpus import wordnet
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag
import spacy
from spacy.matcher import Matcher
from spacy.util import filter_spans

nlp = spacy.load("en_core_web_sm")

# verbPhrasesPattern = [
#     {"POS": "VERB", "OP": "*"},
#     {"POS": "ADP", "OP": "{1}"}
# ]

# sentence = "eat lamb leg and wooden boat"

# matcher = Matcher(nlp.vocab)

# matcher.add("verb-phrases", [verbPhrasesPattern])
# doc = nlp(sentence) 
# tagged_tokens = [(token.text, token.pos_) for token in doc]

# matches = matcher(doc) 
# spans = [doc[start:end] for _, start, end in matches]

# print (filter_spans(spans))

# for chunk in doc.noun_chunks:
#     print(chunk.text)


#Get verb phrases
# def verbPhrasesFinder(phrase):
#     doc = nlp(phrase)
#     verbPhrasesPattern = [
#         {"POS": "VERB", "OP": "{1}"},
#         {"POS": "ADP", "OP": "?"}
#     ]

#     matcher = Matcher(nlp.vocab)
#     matcher.add("verb-phrases", [verbPhrasesPattern])
#     matches = matcher(doc)
#     noisyVerbs = [doc[start:end] for _, start, end in matches]
#     verbPhrases = filter_spans(noisyVerbs)

#     return verbPhrases

# print(verbPhrasesFinder("fill glass bottle with stream"))

# def parameterFinder()

#Break the phrase into words and classify the words into noun, verb and determiner(number).
def grammarClassifier(phrase):
    nounSet = set()
    verbSet = set()
    # detSet = set()
    numSet = set()
    doc = nlp(phrase)

    verbPhrasesPattern = [
        {"POS": "VERB", "OP": "{1}"},
        {"POS": "ADP", "OP": "?"}
    ]

    matcher = Matcher(nlp.vocab)
    matcher.add("verb-phrases", [verbPhrasesPattern])

    matches = matcher(doc) 
    noisyVerbs = [doc[start:end] for _, start, end in matches]
    verbPhrases = filter_spans(noisyVerbs)

    # for chunk in doc.noun_chunks:
    #     print(chunk)
    #     nounSet.add(str(chunk))

    for chunk in doc.noun_chunks:
        if str(chunk) == "rest":
            verbSet.add(str(chunk))
            break
        elif "attack" in str(chunk):
            verbSet.add("attack")
            fixed_noun = str(chunk).replace("attack ", "")
            nounSet.add(fixed_noun)
            break
        elif "equip" in str(chunk):
            verbSet.add("equip")
            fixed_noun = str(chunk).replace("equip ", "")
            nounSet.add(fixed_noun)
            break
        elif "unequip" in str(chunk):
            verbSet.add("unequip")
            fixed_noun = str(chunk).replace("unequip ", "")
            nounSet.add(fixed_noun)
            break
        nounSet.add(str(chunk)) 

    tagged_tokens = [(token.text, token.pos_) for token in doc]
    print(tagged_tokens)

    for token, pos in tagged_tokens:
        if pos.lower() == "adv":
            nounSet.add(str(token))

    for token, pos in tagged_tokens:
        if pos.lower() == "num":
            numSet.add(str(token))

    if len(nounSet) != 0:
        for verbPharse in verbPhrases:
            for noun in nounSet:
                if str(verbPharse) not in noun:
                    verbSet.add(str(verbPharse))
    else:
        for verbPharse in verbPhrases:
            verbSet.add(str(verbPharse))

    grammarDict = {
        "Noun list": nounSet,
        "Verb list": verbSet,
        # "Determiner list": detSet
        "Number list": numSet
    }

    return grammarDict

print(grammarClassifier("go north"))

# take all #
# take lamb leg #
# take glass water bottle #
# equip the sword !
# unequip #
# check player #
# eat soup #
# eat grilled fish #
# attack the wolf !
# rest #
# go forward #
# go back #
# go right #
# go left #
# go north #
# go south #
# go east #
# go west #
# take bottle water #
# take raw venison #
# take palm leaves #
# take weapon crafting bench #
# take bottle of sand !
# take aloe vera #
# eat aloe vera #
# take grilled venison #
# eat grilled venison #









# nlp.add_pipe("textrank")
# doc = nlp("get off wooden boat")
# for chunk in doc.noun_chunks:
#     print(chunk.text)

# for phrase in doc._.phrases:
#     print(phrase.text)

# pattern = [
#     {"POS": "VERB", "OP": "*"},
#     {"POS": "ADP", "OP": "{1}"}
# ]

# sentence = "get on wooden boat"

# matcher = Matcher(nlp.vocab)

# matcher.add("verb-phrases", [pattern])
# doc = nlp(sentence) 
# tagged_tokens = [(token.text, token.pos_) for token in doc]

# matches = matcher(doc) 
# spans = [doc[start:end] for _, start, end in matches]

# print (filter_spans(spans))

# nlp = spacy.load("en_core_web_md")

# def get_word_meaning_in_phrase(phrase, word):
#     tokens = word_tokenize(phrase)
#     doc = nlp(phrase)
#     tagged_tokens = [(token.text, token.pos_) for token in doc]
#     return tagged_tokens
#     word_pos = None
#     for token, pos in tagged_tokens:
#         if token.lower() == word.lower():
#             word_pos = pos
#             break

#     if word_pos:
#         synsets = wordnet.synsets(word, pos=word_pos[0].lower())

#         if synsets:
#             return synsets
#         else:
#             return None
#     else:
#         return None

phrase = "get off wooden boat"

# phrase = input()

# def verbFinder(text):
#     doc = nlp(phrase)
#     tagged_tokens = [(token.text, token.pos_) for token in doc]
#     for token, pos in tagged_tokens:
#         if pos[0].lower() == 'v':
#             return token
# word = verbFinder(phrase)

# synsets = get_word_meaning_in_phrase(phrase, word)

# synonymsList = []

# for synset in synsets:
#     for lemma in synset.lemmas():
#         synonymsList.append(lemma.name())
# print(f"\nSynonyms for '{word}':")
# synonymsList = list(dict.fromkeys(synonymsList))
# print(synonymsList)

# def wordSynonyms(word):
#     synsets = wordnet.synsets(word)
#     synonymsList = []
#     for synset in synsets:
#         for lemma in synset.lemmas():
#             synonymsList.append(lemma.name())
#     print(f"\nSynonyms for '{word}':")
#     synonymsList = list(dict.fromkeys(synonymsList))
#     return synonymsList

# print(wordSynonyms(word))
# def findNoun(phrase):
#     nounSet = set()
#     doc = nlp(phrase)
#     tagged_tokens = [(token.text, token.pos_) for token in doc]
#     for token, pos in tagged_tokens:
#         if pos.lower() == 'noun':
#             nounSet.add(token)
#     return nounSet

# print(findNoun(phrase))

# Break the phrase into words and classify the words into noun, verb and determiner(number).
# def grammarClassifier(phrase):
#     nounSet = set()
#     verbSet = set()
#     detSet = set()
#     doc = nlp(phrase)
#     tagged_tokens = [(token.text, token.pos_) for token in doc]
#     print(tagged_tokens)
#     for token, pos in tagged_tokens:
#         if pos.lower() == 'noun':
#             nounSet.add(token)
#         elif pos.lower() == 'verb':
#             verbSet.add(token)
#         elif pos.lower() == 'det' or pos.lower() == 'num':
#             detSet.add(token)
#     grammarDict = {
#         "Noun list": nounSet,
#         "Verb list": verbSet,
#         "Determiner list": detSet
#     }

#     return grammarDict

# print(grammarClassifier(phrase))

# doc = nlp(phrase)
# tagged_tokens = [(token.text, token.pos_) for token in doc]
    
# for token, pos in tagged_tokens:
#     print(token, pos)


# class action():
#     def __init__(self, actionName: str, tag: [str]) -> None:
#         self.actionName = actionName
#         self.tag = tag
    
# commandTag = {
#     "move": ["move"]
# }

# print(list(command.values())[0][0])

# from nltk.corpus import wordnet as wn
# print(wn.synsets('move'))
# print(wn.synsets('travel'))

# list = set()
# word = "move"
# list.add(word)
# for synsets in wn.synonyms(word):
#     for synset in synsets:
#         list.add(synset)
# print(list)

# input = input()

# if input in list:
#     print(True)
# else:
#     print(False)

# def move(target) -> int: 
#     x = 0
#     y = 0  
#     if target == "North":
#         y = y + 1
#     elif target == "South":
#         y = y - 1
#     elif target == "East":
#         x = x + 1
#     elif target == "West":
#         x = x - 1
    
#     return x,y

# input = input()
# move(input)

# phrase = "move north"
# tagged_tokens = ht.tag(phrase.split())
# print(tagged_tokens)
# ht.close()

# import nltk
# from nltk.corpus import wordnet
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag
# from nltk.tag.hunpos import HunposTagger
# from os.path import expanduser

# def get_word_meaning_in_phrase(phrase, word):
#     tokens = word_tokenize(phrase)
#     home = expanduser("~")
#     _path_to_bin = home + '\\hunpos-1.0-win\\hunpos-tag.exe'
#     _path_to_model = home + '\\hunpos-1.0-win\\english.model'
#     ht = HunposTagger(path_to_model=_path_to_model, path_to_bin=_path_to_bin)
#     tagged_tokens = ht.tag(phrase.split())
#     print(tagged_tokens)
#     ht.close()

#     # 找到目标单词在短语中的词性标签
#     word_pos = None
#     for token, pos in tagged_tokens:
#         if token.lower() == word.lower():
#             word_pos = pos
#             break
    
#     if word_pos:
#         # 根据词性标签在WordNet中找到对应的含义
#         word_pos = str(word_pos, 'utf-8')
#         synsets = wordnet.synsets(word, pos=word_pos[0].lower())
#         if synsets:
#             # 获取短语中其他单词的同义词集合
#             other_words_synsets = []
#             for token, pos in tagged_tokens:
#                 if token.lower() != word.lower():
#                     pos = str(pos, 'utf-8')
#                     synsets2 = wordnet.synsets(token, pos=pos[0].lower())
#                     other_words_synsets.extend(synsets2)
            
#             meanings = [synset.definition() for synset in synsets]
#             return meanings, synsets, other_words_synsets
#         else:
#             return None, None, None
#     else:
#         return None, None, None

# # 示例短语和目标单词
# phrase = "move north"
# word = "move"
# synonymsList = []

# # 获取目标单词在短语中的意思和相应的同义词集合
# meanings, synsets, other_words_synsets = get_word_meaning_in_phrase(phrase, word)
# if meanings:
#     # 显示与给定含义相关的同义词集合
#     for synset in synsets:
#         for lemma in synset.lemmas():
#             synonymsList.append(lemma.name())
#     print(f"\nSynonyms for '{word}':")
#     synonymsList = list(dict.fromkeys(synonymsList))
#     print(synonymsList)
 
#     # 显示短语中其他单词的同义词集合
#     print("\nOther words' synonyms in the context of the phrase:")
#     for other_word_synsets in other_words_synsets:
#         for lemma in other_word_synsets.lemmas():
#             print(lemma.name())
# else:
#     print(f"No meanings found for '{word}' in the context of the phrase")

# import spacy
# import time


# # Load the English language model
# nlp = spacy.load("en_core_web_sm")

# # Define the phrase
# phrase = "rest with bed"
# begin = time.time()
# # Tokenize and tag the phrase
# doc = nlp(phrase)

# # Extract tokens and their POS tags
# tagged_tokens = [(token.text, token.pos_) for token in doc]
# print(time.time()-begin)
# # Print the tagged tokens
# print(tagged_tokens)

# print(wordnet.synonyms("run"))